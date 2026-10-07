'use strict';
const oracledb = require('oracledb');

oracledb.fetchAsString = [oracledb.CLOB];

async function connect(env) {
  const password = resolvePassword(env);
  return oracledb.getConnection({
    user: env.user,
    password,
    connectString: env.connectString,
  });
}

/**
 * Passwords may be given inline (convenient for a throwaway local DB) or, for
 * anything shared, as `env:VAR_NAME` so real credentials stay out of the repo.
 */
function resolvePassword(env) {
  const raw = env.password || '';
  if (raw.startsWith('env:')) {
    const varName = raw.slice(4);
    const value = process.env[varName];
    if (!value) {
      throw new Error(
        `Environment "${env.name}" expects its password in $${varName}, which is not set.`
      );
    }
    return value;
  }
  return raw;
}

async function query(conn, sql, binds = {}) {
  const result = await conn.execute(sql, binds, { outFormat: oracledb.OUT_FORMAT_OBJECT });
  return result.rows || [];
}

module.exports = { connect, query, resolvePassword };
