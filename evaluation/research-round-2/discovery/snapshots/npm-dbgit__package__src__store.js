'use strict';
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { paths } = require('./config');

function ensureStore(root) {
  const p = paths(root);
  fs.mkdirSync(p.snapshots, { recursive: true });
  fs.mkdirSync(p.migrations, { recursive: true });
  if (!fs.existsSync(p.commits)) writeJson(p.commits, []);
  return p;
}

function readJson(file, fallback) {
  if (!fs.existsSync(file)) return fallback;
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function writeJson(file, value) {
  fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n');
}

function loadCommits(root) {
  return readJson(paths(root).commits, []);
}

function saveCommits(root, commits) {
  writeJson(paths(root).commits, commits);
}

function headCommit(root) {
  const commits = loadCommits(root);
  return commits.length ? commits[commits.length - 1] : null;
}

function loadSnapshot(root, snapshotFile) {
  return readJson(path.join(paths(root).snapshots, snapshotFile), null);
}

/** The snapshot HEAD points at, or an empty schema when nothing is committed. */
function headSnapshot(root) {
  const head = headCommit(root);
  if (!head) return emptySnapshot();
  const snapshot = loadSnapshot(root, head.snapshot);
  return snapshot || emptySnapshot();
}

function emptySnapshot() {
  return { schema: null, tables: {}, views: {}, sources: {}, sequences: {}, triggers: {} };
}

function saveSnapshot(root, snapshot, id) {
  const p = ensureStore(root);
  const file = `${id}.json`;
  writeJson(path.join(p.snapshots, file), snapshot);
  return file;
}

function nextCommitId(commits) {
  return String(commits.length + 1).padStart(4, '0');
}

function shortHash(value) {
  return crypto.createHash('sha1').update(value).digest('hex').slice(0, 8);
}

/**
 * Flyway-style versioned filename, so these scripts stay portable.
 *
 * Letters of any script are kept, not just ASCII — a team writing commit
 * messages in Thai would otherwise get a directory full of files all named
 * "change". Combining marks are kept alongside letters, since Thai vowels and
 * tone marks are marks rather than letters and dropping them mangles the word.
 */
function migrationFileName(timestamp, message) {
  const slug =
    String(message)
      .toLowerCase()
      .replace(/[^\p{L}\p{N}\p{M}]+/gu, '_')
      .replace(/^_+|_+$/g, '')
      .slice(0, 60) || 'change';
  return `V${timestamp}__${slug}.sql`;
}

function stampNow(date = new Date()) {
  const pad = (n) => String(n).padStart(2, '0');
  return (
    date.getFullYear() +
    pad(date.getMonth() + 1) +
    pad(date.getDate()) +
    pad(date.getHours()) +
    pad(date.getMinutes()) +
    pad(date.getSeconds())
  );
}

function writeMigration(root, fileName, contents) {
  const p = ensureStore(root);
  const file = path.join(p.migrations, fileName);
  fs.writeFileSync(file, contents);
  return file;
}

function readMigration(root, fileName) {
  const file = path.join(paths(root).migrations, fileName);
  if (!fs.existsSync(file)) return null;
  return fs.readFileSync(file, 'utf8');
}

/**
 * Splits a migration file into executable statements.
 *
 * PL/SQL bodies are delimited by a lone `/` because they contain semicolons of
 * their own; everything else is delimited by `;`.
 */
function splitStatements(sql) {
  const statements = [];
  let buffer = [];
  let inBlock = false;

  // A PL/SQL body ends with its own `END;` that must survive; only the
  // statement-terminating semicolon of plain DDL is stripped.
  const flush = (keepTrailingSemicolon) => {
    const joined = buffer.join('\n').trim();
    const text = keepTrailingSemicolon ? joined : joined.replace(/;$/, '').trim();
    if (text && !isOnlyComments(text)) statements.push(text);
    buffer = [];
  };

  for (const line of sql.split('\n')) {
    const trimmed = line.trim();
    if (trimmed === '/') {
      flush(true);
      inBlock = false;
      continue;
    }
    if (/^(CREATE|DECLARE|BEGIN)\b/i.test(trimmed) && /\b(PROCEDURE|FUNCTION|PACKAGE|TRIGGER|TYPE)\b/i.test(trimmed)) {
      inBlock = true;
    }
    buffer.push(line);
    if (!inBlock && trimmed.endsWith(';')) flush();
  }
  flush();
  return statements;
}

function isOnlyComments(text) {
  return text
    .split('\n')
    .every((line) => line.trim() === '' || line.trim().startsWith('--'));
}

module.exports = {
  ensureStore,
  readJson,
  writeJson,
  loadCommits,
  saveCommits,
  headCommit,
  headSnapshot,
  loadSnapshot,
  saveSnapshot,
  emptySnapshot,
  nextCommitId,
  shortHash,
  migrationFileName,
  stampNow,
  writeMigration,
  readMigration,
  splitStatements,
};
