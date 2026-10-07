'use strict';
const { query } = require('./db');

const LEDGER_TABLE = 'DBGIT_CHANGELOG';

/**
 * Reads an Oracle schema into a canonical, order-independent model.
 *
 * Everything here is keyed by object name rather than stored as arrays, so two
 * snapshots of the same schema compare equal regardless of the order Oracle
 * happened to return rows in. Volatile values (sequence LAST_NUMBER, object
 * timestamps, statistics) are deliberately excluded — they would show up as
 * spurious changes on every single snapshot.
 */
async function introspect(conn, schema) {
  const owner = schema.toUpperCase();
  const [tables, views, sources, sequences, triggers] = await Promise.all([
    readTables(conn, owner),
    readViews(conn, owner),
    readSources(conn, owner),
    readSequences(conn, owner),
    readTriggers(conn, owner),
  ]);
  return { schema: owner, tables, views, sources, sequences, triggers };
}

async function readTables(conn, owner) {
  const tables = {};

  const tableRows = await query(
    conn,
    `SELECT TABLE_NAME FROM ALL_TABLES
      WHERE OWNER = :owner AND TABLE_NAME NOT LIKE 'BIN$%'
        AND TABLE_NAME <> :ledger
      ORDER BY TABLE_NAME`,
    { owner, ledger: LEDGER_TABLE }
  );
  for (const row of tableRows) {
    tables[row.TABLE_NAME] = { columns: {}, primaryKey: null, constraints: {}, indexes: {} };
  }

  const columnRows = await query(
    conn,
    `SELECT TABLE_NAME, COLUMN_NAME, COLUMN_ID, DATA_TYPE, DATA_LENGTH, DATA_PRECISION,
            DATA_SCALE, CHAR_LENGTH, CHAR_USED, NULLABLE, DATA_DEFAULT
       FROM ALL_TAB_COLUMNS
      WHERE OWNER = :owner AND TABLE_NAME NOT LIKE 'BIN$%'
      ORDER BY TABLE_NAME, COLUMN_ID`,
    { owner }
  );
  for (const row of columnRows) {
    const table = tables[row.TABLE_NAME];
    if (!table) continue; // view or materialized-view column
    table.columns[row.COLUMN_NAME] = {
      position: row.COLUMN_ID,
      dataType: row.DATA_TYPE,
      length: row.DATA_LENGTH,
      precision: row.DATA_PRECISION,
      scale: row.DATA_SCALE,
      charLength: row.CHAR_LENGTH,
      charUsed: row.CHAR_USED,
      nullable: row.NULLABLE === 'Y',
      default: normalizeDefault(row.DATA_DEFAULT),
    };
  }

  const constraintRows = await query(
    conn,
    `SELECT c.CONSTRAINT_NAME, c.TABLE_NAME, c.CONSTRAINT_TYPE, c.SEARCH_CONDITION,
            c.GENERATED, c.DELETE_RULE, c.STATUS,
            rc.TABLE_NAME AS REF_TABLE, rc.CONSTRAINT_NAME AS REF_CONSTRAINT
       FROM ALL_CONSTRAINTS c
       LEFT JOIN ALL_CONSTRAINTS rc
         ON rc.OWNER = c.R_OWNER AND rc.CONSTRAINT_NAME = c.R_CONSTRAINT_NAME
      WHERE c.OWNER = :owner AND c.TABLE_NAME NOT LIKE 'BIN$%'
        AND c.CONSTRAINT_TYPE IN ('P', 'U', 'R', 'C')`,
    { owner }
  );

  const consColumnRows = await query(
    conn,
    `SELECT CONSTRAINT_NAME, TABLE_NAME, COLUMN_NAME, POSITION
       FROM ALL_CONS_COLUMNS
      WHERE OWNER = :owner
      ORDER BY CONSTRAINT_NAME, POSITION`,
    { owner }
  );
  const consColumns = groupColumns(consColumnRows, 'CONSTRAINT_NAME');

  for (const row of constraintRows) {
    const table = tables[row.TABLE_NAME];
    if (!table) continue;

    const condition = normalizeText(row.SEARCH_CONDITION);
    // Oracle materialises every NOT NULL as a generated check constraint.
    // The column's own `nullable` flag already carries that information, so
    // keeping these would double-report each nullability change.
    if (row.CONSTRAINT_TYPE === 'C' && isGeneratedNotNull(row.GENERATED, condition)) continue;

    const columns = consColumns[row.CONSTRAINT_NAME] || [];
    const constraint = {
      type: row.CONSTRAINT_TYPE,
      columns,
      enabled: row.STATUS === 'ENABLED',
    };
    if (row.CONSTRAINT_TYPE === 'C') constraint.condition = condition;
    if (row.CONSTRAINT_TYPE === 'R') {
      constraint.refTable = row.REF_TABLE;
      constraint.refColumns = consColumns[row.REF_CONSTRAINT] || [];
      constraint.deleteRule = row.DELETE_RULE;
    }
    table.constraints[row.CONSTRAINT_NAME] = constraint;
    if (row.CONSTRAINT_TYPE === 'P') {
      table.primaryKey = { name: row.CONSTRAINT_NAME, columns };
    }
  }

  const indexRows = await query(
    conn,
    `SELECT i.INDEX_NAME, i.TABLE_NAME, i.UNIQUENESS, i.INDEX_TYPE
       FROM ALL_INDEXES i
      WHERE i.OWNER = :owner AND i.TABLE_NAME NOT LIKE 'BIN$%'`,
    { owner }
  );
  const indexColumnRows = await query(
    conn,
    `SELECT INDEX_NAME, COLUMN_NAME, COLUMN_POSITION AS POSITION, DESCEND
       FROM ALL_IND_COLUMNS
      WHERE INDEX_OWNER = :owner
      ORDER BY INDEX_NAME, COLUMN_POSITION`,
    { owner }
  );
  const indexColumns = groupColumns(indexColumnRows, 'INDEX_NAME');

  for (const row of indexRows) {
    const table = tables[row.TABLE_NAME];
    if (!table) continue;
    // Indexes Oracle created to enforce a PK/UK are already described by the
    // constraint itself; recording them separately would report one change twice.
    if (table.constraints[row.INDEX_NAME]) continue;
    table.indexes[row.INDEX_NAME] = {
      unique: row.UNIQUENESS === 'UNIQUE',
      indexType: row.INDEX_TYPE,
      columns: indexColumns[row.INDEX_NAME] || [],
    };
  }

  return tables;
}

async function readViews(conn, owner) {
  const views = {};
  const rows = await query(
    conn,
    `SELECT VIEW_NAME, TEXT FROM ALL_VIEWS WHERE OWNER = :owner ORDER BY VIEW_NAME`,
    { owner }
  );
  for (const row of rows) {
    views[row.VIEW_NAME] = { text: normalizeText(row.TEXT) };
  }
  return views;
}

/** Packages, procedures, functions and types, reassembled from ALL_SOURCE lines. */
async function readSources(conn, owner) {
  const sources = {};
  const rows = await query(
    conn,
    `SELECT NAME, TYPE, LINE, TEXT
       FROM ALL_SOURCE
      WHERE OWNER = :owner
        AND TYPE IN ('PROCEDURE','FUNCTION','PACKAGE','PACKAGE BODY','TYPE','TYPE BODY')
      ORDER BY NAME, TYPE, LINE`,
    { owner }
  );
  for (const row of rows) {
    const key = `${row.TYPE}:${row.NAME}`;
    if (!sources[key]) sources[key] = { type: row.TYPE, name: row.NAME, lines: [] };
    sources[key].lines.push(row.TEXT);
  }

  const statusRows = await query(
    conn,
    `SELECT OBJECT_NAME, OBJECT_TYPE, STATUS
       FROM ALL_OBJECTS
      WHERE OWNER = :owner
        AND OBJECT_TYPE IN ('PROCEDURE','FUNCTION','PACKAGE','PACKAGE BODY','TYPE','TYPE BODY')`,
    { owner }
  );
  const statuses = {};
  for (const row of statusRows) statuses[`${row.OBJECT_TYPE}:${row.OBJECT_NAME}`] = row.STATUS;

  const result = {};
  for (const [key, value] of Object.entries(sources)) {
    result[key] = {
      type: value.type,
      name: value.name,
      text: normalizeText(value.lines.join('')),
      // Not part of the diff — surfaced in the UI so INVALID objects are visible.
      status: statuses[key] || 'UNKNOWN',
    };
  }
  return result;
}

async function readSequences(conn, owner) {
  const sequences = {};
  const rows = await query(
    conn,
    `SELECT SEQUENCE_NAME, MIN_VALUE, MAX_VALUE, INCREMENT_BY, CYCLE_FLAG, ORDER_FLAG, CACHE_SIZE
       FROM ALL_SEQUENCES WHERE SEQUENCE_OWNER = :owner ORDER BY SEQUENCE_NAME`,
    { owner }
  );
  for (const row of rows) {
    // LAST_NUMBER is intentionally omitted: it advances on every nextval and
    // would make every snapshot differ from the previous one.
    sequences[row.SEQUENCE_NAME] = {
      minValue: String(row.MIN_VALUE),
      maxValue: String(row.MAX_VALUE),
      incrementBy: String(row.INCREMENT_BY),
      cycle: row.CYCLE_FLAG === 'Y',
      ordered: row.ORDER_FLAG === 'Y',
      cacheSize: String(row.CACHE_SIZE),
    };
  }
  return sequences;
}

async function readTriggers(conn, owner) {
  const triggers = {};
  const rows = await query(
    conn,
    `SELECT TRIGGER_NAME, TABLE_NAME, TRIGGER_TYPE, TRIGGERING_EVENT,
            WHEN_CLAUSE, STATUS, DESCRIPTION, TRIGGER_BODY
       FROM ALL_TRIGGERS WHERE OWNER = :owner ORDER BY TRIGGER_NAME`,
    { owner }
  );
  for (const row of rows) {
    triggers[row.TRIGGER_NAME] = {
      table: row.TABLE_NAME,
      triggerType: row.TRIGGER_TYPE,
      event: row.TRIGGERING_EVENT,
      whenClause: normalizeText(row.WHEN_CLAUSE),
      description: normalizeText(row.DESCRIPTION),
      body: normalizeText(row.TRIGGER_BODY),
      status: row.STATUS,
    };
  }
  return triggers;
}

function groupColumns(rows, key) {
  const grouped = {};
  for (const row of rows) {
    if (!grouped[row[key]]) grouped[row[key]] = [];
    grouped[row[key]].push(row.COLUMN_NAME);
  }
  return grouped;
}

/**
 * Oracle pads stored defaults with trailing whitespace and newlines that vary
 * with how the DDL was typed. Trimming keeps `DEFAULT 'Y'` and `DEFAULT 'Y' `
 * from looking like a change.
 */
function normalizeDefault(value) {
  if (value === null || value === undefined) return null;
  const text = String(value).trim();
  return text === '' ? null : text;
}

function normalizeText(value) {
  if (value === null || value === undefined) return null;
  return String(value).replace(/\r\n/g, '\n').trimEnd();
}

function isGeneratedNotNull(generated, condition) {
  if (generated !== 'GENERATED NAME' || !condition) return false;
  return /^"?[A-Za-z0-9_$#]+"?\s+IS\s+NOT\s+NULL$/i.test(condition.trim());
}

module.exports = { introspect, LEDGER_TABLE };
