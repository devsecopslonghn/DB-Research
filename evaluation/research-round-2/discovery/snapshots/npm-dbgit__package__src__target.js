'use strict';
const fs = require('fs');
const path = require('path');
const { formatType, parseType, normalizeColumn } = require('./types');

/**
 * The target schema: what the database is supposed to look like.
 *
 * It lives as ordinary files under schema/ so it can be reviewed in a merge
 * request and merged with the same tools as the application code. Tables become
 * JSON because their structure is what matters; views, program units and
 * triggers stay as .sql because they already are source code.
 *
 * Reading these files reconstructs exactly the shape `introspect()` produces,
 * which is what lets the same diff engine compare target against any database.
 */

const DIRS = {
  tables: 'tables',
  views: 'views',
  sources: 'programs',
  sequences: 'sequences',
  triggers: 'triggers',
};

const SOURCE_DIR_BY_TYPE = {
  PROCEDURE: 'procedures',
  FUNCTION: 'functions',
  PACKAGE: 'packages',
  'PACKAGE BODY': 'package_bodies',
  TYPE: 'types',
  'TYPE BODY': 'type_bodies',
};
const TYPE_BY_SOURCE_DIR = Object.fromEntries(Object.entries(SOURCE_DIR_BY_TYPE).map(([k, v]) => [v, k]));

function schemaDir(root) {
  return path.join(root, 'schema');
}

function exists(root) {
  return fs.existsSync(schemaDir(root));
}

function write(root, snapshot) {
  const base = schemaDir(root);
  fs.rmSync(base, { recursive: true, force: true });

  writeJson(path.join(base, 'schema.json'), { schema: snapshot.schema });

  for (const [name, table] of Object.entries(snapshot.tables || {})) {
    writeJson(path.join(base, DIRS.tables, `${name}.json`), serializeTable(name, table));
  }
  for (const [name, view] of Object.entries(snapshot.views || {})) {
    writeText(path.join(base, DIRS.views, `${name}.sql`), `${view.text}\n`);
  }
  for (const source of Object.values(snapshot.sources || {})) {
    const dir = SOURCE_DIR_BY_TYPE[source.type];
    if (!dir) continue;
    writeText(path.join(base, DIRS.sources, dir, `${source.name}.sql`), `${source.text}\n`);
  }
  for (const [name, sequence] of Object.entries(snapshot.sequences || {})) {
    writeJson(path.join(base, DIRS.sequences, `${name}.json`), sequence);
  }
  for (const [name, trigger] of Object.entries(snapshot.triggers || {})) {
    writeJson(path.join(base, DIRS.triggers, `${name}.json`), {
      table: trigger.table,
      triggerType: trigger.triggerType,
      event: trigger.event,
      whenClause: trigger.whenClause,
      description: trigger.description,
      status: trigger.status,
    });
    writeText(path.join(base, DIRS.triggers, `${name}.sql`), `${trigger.body}\n`);
  }
  return base;
}

function read(root) {
  const base = schemaDir(root);
  if (!fs.existsSync(base)) {
    throw new Error('No schema/ folder found. Run "dbgit baseline" to create it from a database.');
  }

  const meta = readJson(path.join(base, 'schema.json'), { schema: null });
  const snapshot = { schema: meta.schema, tables: {}, views: {}, sources: {}, sequences: {}, triggers: {} };

  for (const file of listFiles(path.join(base, DIRS.tables), '.json')) {
    const name = path.basename(file, '.json');
    try {
      snapshot.tables[name] = deserializeTable(readJson(file));
    } catch (error) {
      throw new Error(`schema/tables/${name}.json: ${error.message}`);
    }
  }
  for (const file of listFiles(path.join(base, DIRS.views), '.sql')) {
    snapshot.views[path.basename(file, '.sql')] = { text: trimEnd(fs.readFileSync(file, 'utf8')) };
  }
  for (const [dir, type] of Object.entries(TYPE_BY_SOURCE_DIR)) {
    for (const file of listFiles(path.join(base, DIRS.sources, dir), '.sql')) {
      const name = path.basename(file, '.sql');
      snapshot.sources[`${type}:${name}`] = {
        type,
        name,
        text: trimEnd(fs.readFileSync(file, 'utf8')),
        status: 'VALID',
      };
    }
  }
  for (const file of listFiles(path.join(base, DIRS.sequences), '.json')) {
    snapshot.sequences[path.basename(file, '.json')] = readJson(file);
  }
  for (const file of listFiles(path.join(base, DIRS.triggers), '.json')) {
    const name = path.basename(file, '.json');
    const meta = readJson(file);
    const bodyFile = path.join(base, DIRS.triggers, `${name}.sql`);
    snapshot.triggers[name] = {
      ...meta,
      body: fs.existsSync(bodyFile) ? trimEnd(fs.readFileSync(bodyFile, 'utf8')) : '',
    };
  }
  return snapshot;
}

/** Writes a single table file, used when the UI edits one table. */
function writeTable(root, name, table) {
  writeJson(path.join(schemaDir(root), DIRS.tables, `${name}.json`), serializeTable(name, table));
}

function removeTable(root, name) {
  fs.rmSync(path.join(schemaDir(root), DIRS.tables, `${name}.json`), { force: true });
}

function serializeTable(name, table) {
  const columns = {};
  const ordered = Object.entries(table.columns).sort((a, b) => (a[1].position || 0) - (b[1].position || 0));
  for (const [columnName, column] of ordered) {
    const entry = { type: formatType(column) };
    if (column.nullable === false) entry.notNull = true;
    if (column.default !== null && column.default !== undefined) entry.default = column.default;
    columns[columnName] = entry;
  }

  const out = { name, columns };
  if (table.primaryKey) {
    out.primaryKey = { name: table.primaryKey.name, columns: table.primaryKey.columns };
  }

  const foreignKeys = {};
  const uniques = {};
  const checks = {};
  for (const [constraintName, constraint] of Object.entries(table.constraints || {})) {
    if (constraint.type === 'P') continue;
    if (constraint.type === 'R') {
      foreignKeys[constraintName] = {
        columns: constraint.columns,
        references: { table: constraint.refTable, columns: constraint.refColumns },
        onDelete: constraint.deleteRule && constraint.deleteRule !== 'NO ACTION' ? constraint.deleteRule : undefined,
      };
    } else if (constraint.type === 'U') {
      uniques[constraintName] = { columns: constraint.columns };
    } else if (constraint.type === 'C') {
      checks[constraintName] = { condition: constraint.condition };
    }
  }
  if (Object.keys(uniques).length) out.unique = uniques;
  if (Object.keys(foreignKeys).length) out.foreignKeys = foreignKeys;
  if (Object.keys(checks).length) out.checks = checks;

  const indexes = {};
  for (const [indexName, index] of Object.entries(table.indexes || {})) {
    indexes[indexName] = index.unique ? { columns: index.columns, unique: true } : { columns: index.columns };
  }
  if (Object.keys(indexes).length) out.indexes = indexes;

  return out;
}

function deserializeTable(data) {
  const table = { columns: {}, primaryKey: null, constraints: {}, indexes: {} };

  let position = 0;
  for (const [columnName, entry] of Object.entries(data.columns || {})) {
    position += 1;
    const parsed = parseType(entry.type);
    table.columns[columnName] = normalizeColumn({
      ...parsed,
      nullable: entry.notNull !== true,
      default: entry.default === undefined ? null : entry.default,
      position,
    });
  }

  if (data.primaryKey) {
    const name = data.primaryKey.name || `PK_${data.name}`;
    const columns = data.primaryKey.columns || [];
    table.primaryKey = { name, columns };
    table.constraints[name] = { type: 'P', columns, enabled: true };
  }
  for (const [name, entry] of Object.entries(data.unique || {})) {
    table.constraints[name] = { type: 'U', columns: entry.columns, enabled: true };
  }
  for (const [name, entry] of Object.entries(data.foreignKeys || {})) {
    table.constraints[name] = {
      type: 'R',
      columns: entry.columns,
      enabled: true,
      refTable: entry.references.table,
      refColumns: entry.references.columns,
      deleteRule: entry.onDelete || 'NO ACTION',
    };
  }
  for (const [name, entry] of Object.entries(data.checks || {})) {
    table.constraints[name] = { type: 'C', columns: [], enabled: true, condition: entry.condition };
  }
  for (const [name, entry] of Object.entries(data.indexes || {})) {
    table.indexes[name] = {
      unique: entry.unique === true,
      indexType: 'NORMAL',
      columns: entry.columns,
    };
  }
  return table;
}

function listFiles(dir, extension) {
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir)
    .filter((file) => file.endsWith(extension))
    .sort()
    .map((file) => path.join(dir, file));
}

function writeJson(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n');
}

function writeText(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, value);
}

function readJson(file, fallback) {
  if (!fs.existsSync(file)) {
    if (fallback !== undefined) return fallback;
    throw new Error(`Missing file ${file}`);
  }
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

const trimEnd = (text) => String(text).replace(/\r\n/g, '\n').trimEnd();

module.exports = { write, read, writeTable, removeTable, exists, schemaDir, serializeTable, deserializeTable };
