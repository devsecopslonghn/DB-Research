'use strict';
const { query } = require('./db');
const { LEDGER_TABLE } = require('./introspect');

/**
 * A deploy log kept inside each environment.
 *
 * It has to live in the database rather than the repo, because it answers
 * "what does UAT2 actually have?" from any machine and any branch. Every deploy
 * appends a row, so redeploying the same commit after resolving drift is
 * recorded rather than hidden.
 */
async function ensureLedger(conn) {
  const existing = await query(conn, `SELECT COUNT(*) AS N FROM USER_TABLES WHERE TABLE_NAME = :name`, {
    name: LEDGER_TABLE,
  });
  if (existing[0].N > 0) return false;

  await conn.execute(`
    CREATE TABLE ${LEDGER_TABLE} (
      DEPLOY_ID       RAW(16)        DEFAULT SYS_GUID() NOT NULL,
      COMMIT_ID       VARCHAR2(40)   NOT NULL,
      MESSAGE         VARCHAR2(1000),
      CHECKSUM        VARCHAR2(64),
      STATEMENT_COUNT NUMBER(8),
      APPLIED_AT      TIMESTAMP      DEFAULT SYSTIMESTAMP NOT NULL,
      APPLIED_BY      VARCHAR2(128),
      DURATION_MS     NUMBER(12),
      CONSTRAINT PK_${LEDGER_TABLE} PRIMARY KEY (DEPLOY_ID)
    )`);
  return true;
}

async function readLedger(conn) {
  await ensureLedger(conn);
  const rows = await query(
    conn,
    `SELECT COMMIT_ID, MESSAGE, CHECKSUM, APPLIED_BY, DURATION_MS, STATEMENT_COUNT,
            TO_CHAR(APPLIED_AT, 'YYYY-MM-DD HH24:MI:SS') AS APPLIED_AT
       FROM ${LEDGER_TABLE} ORDER BY APPLIED_AT`
  );
  return rows.map((row) => ({
    commitId: row.COMMIT_ID,
    message: row.MESSAGE,
    checksum: row.CHECKSUM,
    appliedAt: row.APPLIED_AT,
    appliedBy: row.APPLIED_BY,
    statementCount: row.STATEMENT_COUNT,
    durationMs: row.DURATION_MS,
  }));
}

async function recordDeploy(conn, entry) {
  await conn.execute(
    `INSERT INTO ${LEDGER_TABLE} (COMMIT_ID, MESSAGE, CHECKSUM, STATEMENT_COUNT, APPLIED_BY, DURATION_MS)
     VALUES (:commitId, :message, :checksum, :statementCount, :appliedBy, :durationMs)`,
    {
      commitId: String(entry.commitId),
      message: (entry.message || '').slice(0, 1000),
      checksum: entry.checksum || null,
      statementCount: entry.statementCount || 0,
      appliedBy: (entry.appliedBy || 'dbgit').slice(0, 128),
      durationMs: entry.durationMs || 0,
    },
    { autoCommit: true }
  );
}

/** The commit this environment was last brought up to, if any. */
function currentCommit(history) {
  if (!history || history.length === 0) return null;
  return history[history.length - 1].commitId;
}

/** Commits recorded in this environment that the repo has never heard of. */
function unknownCommits(commits, history) {
  const known = new Set(commits.map((commit) => commit.id));
  const seen = new Set();
  return (history || [])
    .filter((entry) => !known.has(entry.commitId) && !seen.has(entry.commitId) && seen.add(entry.commitId))
    .map((entry) => entry);
}

module.exports = { ensureLedger, readLedger, recordDeploy, currentCommit, unknownCommits, LEDGER_TABLE };
