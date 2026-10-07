'use strict';
const { describeColumn } = require('./diff');

/**
 * Turns diff changes into Oracle DDL.
 *
 * Each statement carries its own terminator style: PL/SQL bodies need a lone
 * slash on the following line, plain DDL needs a semicolon. Keeping that with
 * the statement lets both the file writer and the executor stay simple.
 */
function generateStatements(changes, options = {}) {
  const allowDestructive = options.allowDestructive === true;
  const statements = [];

  for (const change of changes) {
    if (change.destructive && !allowDestructive) {
      statements.push({
        change,
        skipped: true,
        reason: 'destructive',
        sql: `-- SKIPPED (destructive): ${change.summary}\n-- ${destructiveHint(change)}`,
      });
      continue;
    }
    for (const sql of statementsFor(change)) {
      statements.push({ change, skipped: false, ...sql });
    }
  }
  return statements;
}

function statementsFor(change) {
  switch (change.kind) {
    case 'table.add':
      return [plain(createTable(change.table, change.after))];
    case 'table.drop':
      return [plain(`DROP TABLE ${q(change.table)} CASCADE CONSTRAINTS`)];

    case 'column.add':
      return [plain(`ALTER TABLE ${q(change.table)} ADD (${columnDefinition(change.name, change.after)})`)];
    case 'column.drop':
      return [plain(`ALTER TABLE ${q(change.table)} DROP COLUMN ${q(change.name)}`)];
    case 'column.modify':
      return [plain(`ALTER TABLE ${q(change.table)} MODIFY (${modifyClause(change)})`)];

    case 'constraint.add':
      return [plain(addConstraint(change.table, change.name, change.after))];
    case 'constraint.drop':
      return [plain(`ALTER TABLE ${q(change.table)} DROP CONSTRAINT ${q(change.name)}`)];
    case 'constraint.replace':
      return [
        plain(`ALTER TABLE ${q(change.table)} DROP CONSTRAINT ${q(change.name)}`),
        plain(addConstraint(change.table, change.name, change.after)),
      ];

    case 'index.add':
      return [plain(createIndex(change.table, change.name, change.after))];
    case 'index.drop':
      return [plain(`DROP INDEX ${q(change.name)}`)];
    case 'index.replace':
      return [plain(`DROP INDEX ${q(change.name)}`), plain(createIndex(change.table, change.name, change.after))];

    case 'sequence.add':
      return [plain(createSequence(change.name, change.after))];
    case 'sequence.drop':
      return [plain(`DROP SEQUENCE ${q(change.name)}`)];
    case 'sequence.modify':
      return [plain(alterSequence(change.name, change.after))];

    case 'view.add':
    case 'view.modify':
      return [plain(`CREATE OR REPLACE VIEW ${q(change.name)} AS\n${change.after.text}`)];
    case 'view.drop':
      return [plain(`DROP VIEW ${q(change.name)}`)];

    case 'source.add':
    case 'source.modify':
      return [block(`CREATE OR REPLACE ${change.after.text}`)];
    case 'source.drop':
      return [plain(`DROP ${change.sourceType} ${q(change.name)}`)];

    case 'trigger.add':
    case 'trigger.modify':
      return [block(createTrigger(change.after))];
    case 'trigger.drop':
      return [plain(`DROP TRIGGER ${q(change.name)}`)];

    default:
      return [
        {
          sql: `-- No generator for change kind "${change.kind}": ${change.summary}`,
          terminator: '',
        },
      ];
  }
}

function createTable(name, table) {
  const columns = Object.entries(table.columns)
    .sort((a, b) => a[1].position - b[1].position)
    .map(([columnName, column]) => `  ${columnDefinition(columnName, column)}`);

  const inline = [];
  for (const [constraintName, constraint] of Object.entries(table.constraints || {})) {
    if (constraint.type === 'P' || constraint.type === 'U') {
      const keyword = constraint.type === 'P' ? 'PRIMARY KEY' : 'UNIQUE';
      inline.push(`  CONSTRAINT ${q(constraintName)} ${keyword} (${constraint.columns.map(q).join(', ')})`);
    }
  }
  // Foreign keys are emitted separately by the constraint.add changes so a new
  // table never depends on the creation order of the table it references.
  return `CREATE TABLE ${q(name)} (\n${[...columns, ...inline].join(',\n')}\n)`;
}

function columnDefinition(name, column) {
  let sql = `${q(name)} ${dataType(column)}`;
  if (column.default !== null) sql += ` DEFAULT ${column.default}`;
  if (!column.nullable) sql += ' NOT NULL';
  return sql;
}

function dataType(column) {
  const type = column.dataType;
  if (/^(VARCHAR2|NVARCHAR2|CHAR|NCHAR)$/.test(type)) {
    const size = column.charUsed === 'C' ? `${column.charLength} CHAR` : `${column.length} BYTE`;
    return `${type}(${size})`;
  }
  if (type === 'RAW') return `RAW(${column.length})`;
  if (type === 'NUMBER') {
    if (column.precision === null || column.precision === undefined) return 'NUMBER';
    return column.scale ? `NUMBER(${column.precision},${column.scale})` : `NUMBER(${column.precision})`;
  }
  if (/^TIMESTAMP/.test(type) || /^INTERVAL/.test(type)) return type;
  return type;
}

/**
 * MODIFY only needs the attributes that actually changed. Restating NOT NULL on
 * a column that was already NOT NULL is legal but noisy in a reviewed script.
 */
function modifyClause(change) {
  const to = change.after;
  const fields = change.fields || [];
  const typeChanged = fields.some((f) => ['dataType', 'length', 'precision', 'scale', 'charLength', 'charUsed'].includes(f));

  let sql = q(change.name);
  if (typeChanged) sql += ` ${dataType(to)}`;
  if (fields.includes('default')) sql += ` DEFAULT ${to.default === null ? 'NULL' : to.default}`;
  if (fields.includes('nullable')) sql += to.nullable ? ' NULL' : ' NOT NULL';
  return sql;
}

function addConstraint(table, name, constraint) {
  const base = `ALTER TABLE ${q(table)} ADD CONSTRAINT ${q(name)}`;
  const columns = (constraint.columns || []).map(q).join(', ');
  switch (constraint.type) {
    case 'P':
      return `${base} PRIMARY KEY (${columns})`;
    case 'U':
      return `${base} UNIQUE (${columns})`;
    case 'R': {
      const refColumns = (constraint.refColumns || []).map(q).join(', ');
      const rule = constraint.deleteRule && constraint.deleteRule !== 'NO ACTION' ? ` ON DELETE ${constraint.deleteRule}` : '';
      return `${base} FOREIGN KEY (${columns}) REFERENCES ${q(constraint.refTable)} (${refColumns})${rule}`;
    }
    case 'C':
      return `${base} CHECK (${constraint.condition})`;
    default:
      return `-- Unsupported constraint type "${constraint.type}" for ${name}`;
  }
}

function createIndex(table, name, index) {
  const unique = index.unique ? 'UNIQUE ' : '';
  return `CREATE ${unique}INDEX ${q(name)} ON ${q(table)} (${index.columns.map(q).join(', ')})`;
}

function createSequence(name, sequence) {
  const parts = [`CREATE SEQUENCE ${q(name)}`];
  parts.push(`  INCREMENT BY ${sequence.incrementBy}`);
  parts.push(`  MINVALUE ${sequence.minValue}`);
  parts.push(`  MAXVALUE ${sequence.maxValue}`);
  parts.push(`  ${sequence.cycle ? 'CYCLE' : 'NOCYCLE'}`);
  parts.push(`  ${sequence.ordered ? 'ORDER' : 'NOORDER'}`);
  parts.push(`  ${Number(sequence.cacheSize) > 0 ? `CACHE ${sequence.cacheSize}` : 'NOCACHE'}`);
  return parts.join('\n');
}

function alterSequence(name, sequence) {
  // START WITH cannot be altered, so it is deliberately absent here.
  return [
    `ALTER SEQUENCE ${q(name)}`,
    `  INCREMENT BY ${sequence.incrementBy}`,
    `  MAXVALUE ${sequence.maxValue}`,
    `  ${sequence.cycle ? 'CYCLE' : 'NOCYCLE'}`,
    `  ${Number(sequence.cacheSize) > 0 ? `CACHE ${sequence.cacheSize}` : 'NOCACHE'}`,
  ].join('\n');
}

function createTrigger(trigger) {
  // DESCRIPTION already carries the trigger name, timing, event and FOR EACH ROW.
  const header = (trigger.description || '').trim();
  const when = trigger.whenClause ? `WHEN (${trigger.whenClause})\n` : '';
  return `CREATE OR REPLACE TRIGGER ${header}\n${when}${trigger.body}`;
}

function destructiveHint(change) {
  if (change.kind === 'column.drop') return 'Data in this column will be lost. Re-run with destructive changes allowed to generate it.';
  if (change.kind === 'table.drop') return 'All rows in this table will be lost. Re-run with destructive changes allowed to generate it.';
  if (change.kind === 'column.modify') return 'This narrows the column and may fail or truncate against existing rows.';
  return 'Re-run with destructive changes allowed to generate this statement.';
}

const plain = (sql) => ({ sql, terminator: ';' });
const block = (sql) => ({ sql, terminator: '\n/' });

/** Quote only when the identifier is not a plain uppercase Oracle name. */
function q(identifier) {
  if (/^[A-Z][A-Z0-9_$#]*$/.test(identifier) && identifier.length <= 30) return identifier;
  return `"${identifier}"`;
}

module.exports = { generateStatements, q, dataType, columnDefinition };
