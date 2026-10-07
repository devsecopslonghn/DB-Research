'use strict';

/**
 * Compares two canonical snapshots and returns a flat, ordered list of changes.
 *
 * `destructive` marks anything that can lose data. Those changes are still
 * reported (you need to see them), but the SQL generator refuses to emit them
 * unless explicitly allowed.
 */
function diffSnapshots(before, after) {
  const changes = [];
  diffTables(before.tables || {}, after.tables || {}, changes);
  diffSequences(before.sequences || {}, after.sequences || {}, changes);
  diffViews(before.views || {}, after.views || {}, changes);
  diffSources(before.sources || {}, after.sources || {}, changes);
  diffTriggers(before.triggers || {}, after.triggers || {}, changes);
  return changes.sort(byApplyOrder);
}

function diffTables(before, after, changes) {
  for (const name of added(before, after)) {
    changes.push({
      kind: 'table.add',
      object: name,
      table: name,
      destructive: false,
      after: after[name],
      summary: `new table ${name}`,
    });
    // CREATE TABLE inlines the primary key and unique constraints, but foreign
    // keys and indexes have to follow as their own statements — a foreign key
    // may point at a table created later in the same deploy.
    for (const [constraintName, constraint] of Object.entries(after[name].constraints || {})) {
      if (constraint.type === 'P' || constraint.type === 'U') continue;
      changes.push({
        kind: 'constraint.add',
        object: `${name}.${constraintName}`,
        table: name,
        name: constraintName,
        destructive: false,
        after: constraint,
        summary: `added ${constraintKind(constraint)} ${constraintName} on ${name}`,
      });
    }
    for (const [indexName, index] of Object.entries(after[name].indexes || {})) {
      changes.push({
        kind: 'index.add',
        object: `${name}.${indexName}`,
        table: name,
        name: indexName,
        destructive: false,
        after: index,
        summary: `added index ${indexName} on ${name} (${index.columns.join(', ')})`,
      });
    }
  }
  for (const name of removed(before, after)) {
    changes.push({
      kind: 'table.drop',
      object: name,
      table: name,
      destructive: true,
      before: before[name],
      summary: `dropped table ${name}`,
    });
  }
  for (const name of common(before, after)) {
    diffColumns(name, before[name].columns, after[name].columns, changes);
    diffConstraints(name, before[name].constraints, after[name].constraints, changes);
    diffIndexes(name, before[name].indexes, after[name].indexes, changes);
  }
}

function diffColumns(table, before, after, changes) {
  for (const name of added(before, after)) {
    changes.push({
      kind: 'column.add',
      object: `${table}.${name}`,
      table,
      name,
      destructive: false,
      after: after[name],
      summary: `added column ${table}.${name} ${describeColumn(after[name])}`,
    });
  }
  for (const name of removed(before, after)) {
    changes.push({
      kind: 'column.drop',
      object: `${table}.${name}`,
      table,
      name,
      destructive: true,
      before: before[name],
      summary: `dropped column ${table}.${name}`,
    });
  }
  for (const name of common(before, after)) {
    const from = before[name];
    const to = after[name];
    // `position` shifts whenever an earlier column is dropped; it is not itself
    // a schema change and Oracle offers no way to reorder columns anyway.
    const fields = ['dataType', 'length', 'precision', 'scale', 'charLength', 'charUsed', 'nullable', 'default'];
    const changed = fields.filter((f) => !valuesEqual(from[f], to[f]));
    if (changed.length === 0) continue;
    changes.push({
      kind: 'column.modify',
      object: `${table}.${name}`,
      table,
      name,
      destructive: isNarrowing(from, to),
      before: from,
      after: to,
      fields: changed,
      summary: `changed column ${table}.${name}: ${describeColumn(from)} -> ${describeColumn(to)}`,
    });
  }
}

function diffConstraints(table, before, after, changes) {
  for (const name of added(before, after)) {
    changes.push({
      kind: 'constraint.add',
      object: `${table}.${name}`,
      table,
      name,
      destructive: false,
      after: after[name],
      summary: `added ${constraintKind(after[name])} ${name} on ${table}`,
    });
  }
  for (const name of removed(before, after)) {
    changes.push({
      kind: 'constraint.drop',
      object: `${table}.${name}`,
      table,
      name,
      destructive: true,
      before: before[name],
      summary: `dropped ${constraintKind(before[name])} ${name} on ${table}`,
    });
  }
  for (const name of common(before, after)) {
    if (deepEqual(before[name], after[name])) continue;
    // Oracle has no ALTER CONSTRAINT for definition changes, so this becomes a
    // drop-then-recreate pair at generation time.
    changes.push({
      kind: 'constraint.replace',
      object: `${table}.${name}`,
      table,
      name,
      destructive: true,
      before: before[name],
      after: after[name],
      summary: `redefined ${constraintKind(after[name])} ${name} on ${table}`,
    });
  }
}

function diffIndexes(table, before, after, changes) {
  for (const name of added(before, after)) {
    changes.push({
      kind: 'index.add',
      object: `${table}.${name}`,
      table,
      name,
      destructive: false,
      after: after[name],
      summary: `added index ${name} on ${table} (${after[name].columns.join(', ')})`,
    });
  }
  for (const name of removed(before, after)) {
    changes.push({
      kind: 'index.drop',
      object: `${table}.${name}`,
      table,
      name,
      destructive: true,
      before: before[name],
      summary: `dropped index ${name} on ${table}`,
    });
  }
  for (const name of common(before, after)) {
    if (deepEqual(before[name], after[name])) continue;
    changes.push({
      kind: 'index.replace',
      object: `${table}.${name}`,
      table,
      name,
      destructive: true,
      before: before[name],
      after: after[name],
      summary: `redefined index ${name} on ${table}`,
    });
  }
}

function diffSequences(before, after, changes) {
  for (const name of added(before, after)) {
    changes.push({ kind: 'sequence.add', object: name, name, destructive: false, after: after[name], summary: `added sequence ${name}` });
  }
  for (const name of removed(before, after)) {
    changes.push({ kind: 'sequence.drop', object: name, name, destructive: true, before: before[name], summary: `dropped sequence ${name}` });
  }
  for (const name of common(before, after)) {
    if (deepEqual(before[name], after[name])) continue;
    changes.push({ kind: 'sequence.modify', object: name, name, destructive: false, before: before[name], after: after[name], summary: `changed sequence ${name}` });
  }
}

function diffViews(before, after, changes) {
  for (const name of added(before, after)) {
    changes.push({ kind: 'view.add', object: name, name, destructive: false, after: after[name], summary: `added view ${name}` });
  }
  for (const name of removed(before, after)) {
    changes.push({ kind: 'view.drop', object: name, name, destructive: true, before: before[name], summary: `dropped view ${name}` });
  }
  for (const name of common(before, after)) {
    if (normalizeSql(before[name].text) === normalizeSql(after[name].text)) continue;
    changes.push({ kind: 'view.modify', object: name, name, destructive: false, before: before[name], after: after[name], summary: `changed view ${name}` });
  }
}

function diffSources(before, after, changes) {
  for (const key of added(before, after)) {
    const item = after[key];
    changes.push({ kind: 'source.add', object: key, name: item.name, sourceType: item.type, destructive: false, after: item, summary: `added ${item.type.toLowerCase()} ${item.name}` });
  }
  for (const key of removed(before, after)) {
    const item = before[key];
    changes.push({ kind: 'source.drop', object: key, name: item.name, sourceType: item.type, destructive: true, before: item, summary: `dropped ${item.type.toLowerCase()} ${item.name}` });
  }
  for (const key of common(before, after)) {
    if (normalizeSql(before[key].text) === normalizeSql(after[key].text)) continue;
    const item = after[key];
    changes.push({ kind: 'source.modify', object: key, name: item.name, sourceType: item.type, destructive: false, before: before[key], after: item, summary: `changed ${item.type.toLowerCase()} ${item.name}` });
  }
}

function diffTriggers(before, after, changes) {
  for (const name of added(before, after)) {
    changes.push({ kind: 'trigger.add', object: name, name, destructive: false, after: after[name], summary: `added trigger ${name}` });
  }
  for (const name of removed(before, after)) {
    changes.push({ kind: 'trigger.drop', object: name, name, destructive: true, before: before[name], summary: `dropped trigger ${name}` });
  }
  for (const name of common(before, after)) {
    const a = before[name];
    const b = after[name];
    if (normalizeSql(a.body) === normalizeSql(b.body) && a.event === b.event && a.triggerType === b.triggerType && normalizeSql(a.whenClause) === normalizeSql(b.whenClause)) continue;
    changes.push({ kind: 'trigger.modify', object: name, name, destructive: false, before: a, after: b, summary: `changed trigger ${name}` });
  }
}

/**
 * Dependencies decide the order: tables must exist before their constraints,
 * and referencing objects must be dropped before what they reference.
 */
const APPLY_ORDER = [
  'table.add', 'column.add', 'column.modify', 'sequence.add', 'sequence.modify',
  'index.drop', 'index.replace', 'index.add',
  'constraint.drop', 'constraint.replace', 'constraint.add',
  'column.drop', 'table.drop', 'sequence.drop',
  'view.drop', 'view.add', 'view.modify',
  'source.drop', 'source.add', 'source.modify',
  'trigger.drop', 'trigger.add', 'trigger.modify',
];

function byApplyOrder(a, b) {
  const rank = APPLY_ORDER.indexOf(a.kind) - APPLY_ORDER.indexOf(b.kind);
  if (rank !== 0) return rank;
  return a.object.localeCompare(b.object);
}

/** A shrinking width or a new NOT NULL can fail or truncate against real data. */
function isNarrowing(from, to) {
  if (from.dataType !== to.dataType) return true;
  if (from.nullable && !to.nullable) return true;
  const width = (c) => c.charLength || c.length || 0;
  if (width(to) < width(from)) return true;
  if ((to.precision || 0) < (from.precision || 0)) return true;
  return false;
}

function describeColumn(column) {
  let text = column.dataType;
  if (/CHAR|RAW/.test(column.dataType)) {
    text += `(${column.charLength || column.length}${column.charUsed === 'C' ? ' CHAR' : column.charUsed === 'B' ? ' BYTE' : ''})`;
  } else if (column.dataType === 'NUMBER' && column.precision !== null) {
    text += column.scale ? `(${column.precision},${column.scale})` : `(${column.precision})`;
  }
  if (column.default !== null) text += ` DEFAULT ${column.default}`;
  text += column.nullable ? ' NULL' : ' NOT NULL';
  return text;
}

function constraintKind(constraint) {
  return { P: 'primary key', U: 'unique constraint', R: 'foreign key', C: 'check constraint' }[constraint.type] || 'constraint';
}

/** Whitespace and case differences in PL/SQL are not schema changes. */
function normalizeSql(text) {
  if (text === null || text === undefined) return '';
  return String(text).replace(/\s+/g, ' ').trim().toUpperCase();
}

function valuesEqual(a, b) {
  if (a === null || a === undefined) return b === null || b === undefined;
  return String(a) === String(b);
}

function deepEqual(a, b) {
  return JSON.stringify(sortKeys(a)) === JSON.stringify(sortKeys(b));
}

function sortKeys(value) {
  if (Array.isArray(value)) return value.map(sortKeys);
  if (value && typeof value === 'object') {
    return Object.keys(value).sort().reduce((acc, key) => {
      acc[key] = sortKeys(value[key]);
      return acc;
    }, {});
  }
  return value;
}

const added = (before, after) => Object.keys(after).filter((k) => !(k in before)).sort();
const removed = (before, after) => Object.keys(before).filter((k) => !(k in after)).sort();
const common = (before, after) => Object.keys(after).filter((k) => k in before).sort();

module.exports = { diffSnapshots, describeColumn, constraintKind };
