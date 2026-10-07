'use strict';
const { formatType } = require('./types');
const { constraintKind } = require('./diff');

/**
 * Three-way comparison between the target schema and a live environment.
 *
 * The last committed snapshot is the common ancestor, exactly as in a git
 * merge. Without it there is no way to tell "I added this column" from "someone
 * added this column in UAT" — both look like a difference. With it:
 *
 *   env == base, target != base   -> we changed it; safe to push
 *   env != base, target == base   -> the environment drifted; ask
 *   both moved, and they disagree -> a real conflict; ask
 *   env == target                 -> already in sync; nothing to do
 */

const FORWARD = 'forward';
const ENV_ONLY = 'env_only';
const CONFLICT = 'conflict';

function analyze({ base, target, env, envName }) {
  const locators = new Set([...collect(base).keys(), ...collect(target).keys(), ...collect(env).keys()]);
  const baseMap = collect(base);
  const targetMap = collect(target);
  const envMap = collect(env);

  const forward = [];
  const conflicts = [];

  for (const locator of [...locators].sort()) {
    const baseValue = baseMap.get(locator);
    const targetValue = targetMap.get(locator);
    const envValue = envMap.get(locator);

    if (same(targetValue, envValue)) continue;

    const targetMoved = !same(targetValue, baseValue);
    const envMoved = !same(envValue, baseValue);

    const item = {
      locator,
      ...describe(locator, { base: baseValue, target: targetValue, env: envValue }),
      base: baseValue === undefined ? null : baseValue,
      target: targetValue === undefined ? null : targetValue,
      env: envValue === undefined ? null : envValue,
      envName,
    };

    if (targetMoved && !envMoved) {
      forward.push({ ...item, category: FORWARD });
    } else if (envMoved && !targetMoved) {
      conflicts.push({ ...item, category: ENV_ONLY });
    } else {
      conflicts.push({ ...item, category: CONFLICT });
    }
  }

  return { forward, conflicts, envName };
}

/**
 * Flattens a snapshot into comparable values keyed by a stable locator.
 *
 * Granularity is deliberately per-column and per-index rather than per-table:
 * a decision about one drifted column should not force a decision about the
 * whole table.
 */
function collect(snapshot) {
  const map = new Map();
  if (!snapshot) return map;

  for (const [tableName, table] of Object.entries(snapshot.tables || {})) {
    map.set(`table:${tableName}`, { exists: true });
    for (const [columnName, column] of Object.entries(table.columns || {})) {
      map.set(`column:${tableName}.${columnName}`, {
        type: formatType(column),
        notNull: column.nullable === false,
        default: column.default === null ? undefined : column.default,
      });
    }
    for (const [name, constraint] of Object.entries(table.constraints || {})) {
      map.set(`constraint:${tableName}.${name}`, {
        type: constraint.type,
        columns: constraint.columns,
        refTable: constraint.refTable,
        refColumns: constraint.refColumns,
        deleteRule: constraint.deleteRule,
        condition: constraint.condition,
      });
    }
    for (const [name, index] of Object.entries(table.indexes || {})) {
      map.set(`index:${tableName}.${name}`, { columns: index.columns, unique: index.unique === true });
    }
  }
  for (const [name, view] of Object.entries(snapshot.views || {})) {
    map.set(`view:${name}`, { text: normalize(view.text) });
  }
  for (const [key, source] of Object.entries(snapshot.sources || {})) {
    map.set(`source:${key}`, { text: normalize(source.text) });
  }
  for (const [name, sequence] of Object.entries(snapshot.sequences || {})) {
    map.set(`sequence:${name}`, sequence);
  }
  for (const [name, trigger] of Object.entries(snapshot.triggers || {})) {
    map.set(`trigger:${name}`, {
      table: trigger.table,
      event: trigger.event,
      triggerType: trigger.triggerType,
      body: normalize(trigger.body),
    });
  }
  return map;
}

function describe(locator, values) {
  const [kind, rest] = splitLocator(locator);
  const label = {
    table: 'table',
    column: 'column',
    constraint: 'constraint',
    index: 'index',
    view: 'view',
    source: 'program unit',
    sequence: 'sequence',
    trigger: 'trigger',
  }[kind] || kind;

  const present = (value) => value !== undefined && value !== null;
  let action;
  if (!present(values.env)) action = 'missing_in_env';
  else if (!present(values.target)) action = 'missing_in_target';
  else action = 'differs';

  return {
    kind,
    name: rest,
    label,
    action,
    summary: summarize(kind, rest, label, action, values),
    targetText: renderValue(kind, values.target),
    envText: renderValue(kind, values.env),
  };
}

function summarize(kind, name, label, action, values) {
  if (action === 'missing_in_env') return `${label} ${name} exists in the target but not in the environment`;
  if (action === 'missing_in_target') return `${label} ${name} exists in the environment but not in the target`;
  if (kind === 'column') return `column ${name} differs: target ${renderValue(kind, values.target)} / environment ${renderValue(kind, values.env)}`;
  return `${label} ${name} differs between the target and the environment`;
}

function renderValue(kind, value) {
  if (value === undefined || value === null) return null;
  if (kind === 'column') {
    let text = value.type;
    if (value.default !== undefined) text += ` DEFAULT ${value.default}`;
    text += value.notNull ? ' NOT NULL' : ' NULL';
    return text;
  }
  if (kind === 'index') return `${value.unique ? 'UNIQUE ' : ''}(${(value.columns || []).join(', ')})`;
  if (kind === 'constraint') {
    const base = constraintKind({ type: value.type });
    const columns = (value.columns || []).join(', ');
    if (value.type === 'R') return `${base} (${columns}) -> ${value.refTable} (${(value.refColumns || []).join(', ')})`;
    if (value.type === 'C') return `${base} ${value.condition}`;
    return `${base} (${columns})`;
  }
  if (kind === 'view' || kind === 'source' || kind === 'trigger') {
    const text = value.text || value.body || '';
    return text.length > 400 ? text.slice(0, 400) + '\n...' : text;
  }
  if (kind === 'table') return 'exists';
  return JSON.stringify(value);
}

/**
 * Produces the schema to deploy toward, given a decision per conflict.
 *
 * `take_target` leaves the target value in place. `take_env` and `skip` both
 * substitute the environment's value, which makes the generated diff empty for
 * that object — the difference between them is that `take_env` also writes the
 * value back into schema/, while `skip` leaves the target file untouched so the
 * conflict is raised again next time.
 */
function resolve({ target, env, conflicts, decisions }) {
  const forDeploy = clone(target);
  const forTarget = clone(target);
  const unresolved = [];

  for (const conflict of conflicts) {
    const decision = decisions[conflict.locator] || 'skip';
    if (decision === 'take_target') continue;

    const envValue = readAt(env, conflict.locator);
    applyAt(forDeploy, conflict.locator, envValue, env);
    if (decision === 'take_env') {
      applyAt(forTarget, conflict.locator, envValue, env);
    } else {
      unresolved.push(conflict.locator);
    }
  }
  return { forDeploy, forTarget, unresolved };
}

function splitLocator(locator) {
  const index = locator.indexOf(':');
  return [locator.slice(0, index), locator.slice(index + 1)];
}

/** Reads the raw (not flattened) definition an environment holds at a locator. */
function readAt(snapshot, locator) {
  const [kind, rest] = splitLocator(locator);
  switch (kind) {
    case 'table':
      return (snapshot.tables || {})[rest];
    case 'column': {
      const [table, column] = splitLast(rest);
      return ((snapshot.tables || {})[table] || { columns: {} }).columns[column];
    }
    case 'constraint': {
      const [table, name] = splitLast(rest);
      return ((snapshot.tables || {})[table] || { constraints: {} }).constraints[name];
    }
    case 'index': {
      const [table, name] = splitLast(rest);
      return ((snapshot.tables || {})[table] || { indexes: {} }).indexes[name];
    }
    case 'view':
      return (snapshot.views || {})[rest];
    case 'source':
      return (snapshot.sources || {})[rest];
    case 'sequence':
      return (snapshot.sequences || {})[rest];
    case 'trigger':
      return (snapshot.triggers || {})[rest];
    default:
      return undefined;
  }
}

function applyAt(snapshot, locator, value, envSnapshot) {
  const [kind, rest] = splitLocator(locator);
  const remove = value === undefined || value === null;

  switch (kind) {
    case 'table': {
      if (remove) delete snapshot.tables[rest];
      else snapshot.tables[rest] = clone(value);
      return;
    }
    case 'column':
    case 'constraint':
    case 'index': {
      const [tableName, name] = splitLast(rest);
      const section = { column: 'columns', constraint: 'constraints', index: 'indexes' }[kind];
      if (!snapshot.tables[tableName]) {
        // The whole table only exists in the environment; bring it across so the
        // column has somewhere to live.
        const envTable = (envSnapshot.tables || {})[tableName];
        if (!envTable) return;
        snapshot.tables[tableName] = { columns: {}, primaryKey: null, constraints: {}, indexes: {} };
      }
      const table = snapshot.tables[tableName];
      if (!table[section]) table[section] = {};
      if (remove) delete table[section][name];
      else table[section][name] = clone(value);
      if (kind === 'constraint') {
        table.primaryKey = findPrimaryKey(table);
      }
      return;
    }
    default: {
      const section = { view: 'views', source: 'sources', sequence: 'sequences', trigger: 'triggers' }[kind];
      if (!section) return;
      if (!snapshot[section]) snapshot[section] = {};
      if (remove) delete snapshot[section][rest];
      else snapshot[section][rest] = clone(value);
    }
  }
}

function findPrimaryKey(table) {
  for (const [name, constraint] of Object.entries(table.constraints || {})) {
    if (constraint.type === 'P') return { name, columns: constraint.columns };
  }
  return null;
}

function splitLast(text) {
  const index = text.lastIndexOf('.');
  return [text.slice(0, index), text.slice(index + 1)];
}

function same(a, b) {
  if (a === undefined || a === null) return b === undefined || b === null;
  if (b === undefined || b === null) return false;
  return JSON.stringify(sortKeys(a)) === JSON.stringify(sortKeys(b));
}

function sortKeys(value) {
  if (Array.isArray(value)) return value.map(sortKeys);
  if (value && typeof value === 'object') {
    return Object.keys(value)
      .filter((key) => value[key] !== undefined)
      .sort()
      .reduce((acc, key) => {
        acc[key] = sortKeys(value[key]);
        return acc;
      }, {});
  }
  return value;
}

const clone = (value) => JSON.parse(JSON.stringify(value));
const normalize = (text) => String(text || '').replace(/\s+/g, ' ').trim().toUpperCase();

module.exports = { analyze, resolve, collect, FORWARD, ENV_ONLY, CONFLICT };
