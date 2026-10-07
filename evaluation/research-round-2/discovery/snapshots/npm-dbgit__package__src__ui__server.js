'use strict';
const http = require('http');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const { getEnv } = require('../config');
const store = require('../store');
const engine = require('../engine');
const target = require('../target');
const { readLedger, currentCommit, unknownCommits } = require('../ledger');

function startServer({ root, config, port, open }) {
  const server = http.createServer((req, res) => {
    handle(req, res, { root, config }).catch((error) => send(res, 400, { error: error.message }));
  });

  return new Promise((resolve, reject) => {
    server.on('error', (error) => {
      if (error.code === 'EADDRINUSE') {
        reject(new Error(`Port ${port} is already in use. Start with --port <other> instead.`));
      } else reject(error);
    });
    // Bound to loopback: the UI can change schemas and deploy, so it must not
    // be reachable from the network.
    server.listen(port, '127.0.0.1', () => {
      const url = `http://127.0.0.1:${port}`;
      console.log(`\n  dbgit UI  ${url}`);
      console.log(`  environments: ${Object.keys(config.environments).join(', ')}`);
      console.log('\n  Ctrl+C to stop.\n');
      if (open) exec(`open ${url}`, () => {});
      resolve(server);
    });
  });
}

async function handle(req, res, ctx) {
  const url = new URL(req.url, 'http://localhost');
  const route = url.pathname;

  if (route === '/' || route === '/index.html') {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(fs.readFileSync(path.join(__dirname, 'public', 'index.html')));
    return;
  }
  if (!route.startsWith('/api/')) return send(res, 404, { error: 'Not found' });

  const body = req.method === 'POST' ? await readBody(req) : {};
  const envName = body.env || url.searchParams.get('env') || undefined;
  const env = () => getEnv(ctx.config, envName);

  switch (route) {
    case '/api/state': {
      const commits = store.loadCommits(ctx.root);
      const { changes } = engine.getStatus(ctx.root);
      return send(res, 200, {
        environments: Object.entries(ctx.config.environments).map(([name, value]) => ({
          name,
          schema: value.schema,
          connectString: value.connectString,
          isDefault: name === ctx.config.defaultEnv,
        })),
        defaultEnv: ctx.config.defaultEnv,
        head: commits.length ? commits[commits.length - 1] : null,
        commitCount: commits.length,
        pendingChanges: changes.length,
      });
    }

    case '/api/schema':
      // Reads schema/ from disk — no database connection needed, so browsing
      // stays instant even against a large schema.
      return send(res, 200, summarize(target.read(ctx.root)));

    case '/api/table': {
      const desired = target.read(ctx.root);
      const name = url.searchParams.get('name');
      const table = desired.tables[name];
      if (!table) return send(res, 404, { error: `Table ${name} is not in the target schema.` });
      const { changes } = engine.getStatus(ctx.root);
      return send(res, 200, {
        name,
        table: target.serializeTable(name, table),
        changes: changes.filter((change) => change.table === name),
      });
    }

    case '/api/object': {
      const desired = target.read(ctx.root);
      const kind = url.searchParams.get('kind');
      const key = url.searchParams.get('key');
      const section = { view: 'views', source: 'sources', sequence: 'sequences', trigger: 'triggers' }[kind];
      const object = section ? desired[section][key] : null;
      if (!object) return send(res, 404, { error: `${kind} ${key} was not found.` });
      return send(res, 200, { kind, key, object });
    }

    case '/api/changes': {
      const { changes, desired, head } = engine.getStatus(ctx.root);
      const { sql } = engine.buildMigrationSql(
        changes,
        { allowDestructive: url.searchParams.get('destructive') === '1' },
        { commitId: '(uncommitted)', message: 'uncommitted changes', createdAt: new Date().toISOString(), author: 'dbgit-ui', schema: desired.schema }
      );
      return send(res, 200, { changes, sql, head });
    }

    case '/api/edit': {
      engine.editTarget(ctx.root, body.intent || {});
      const { changes } = engine.getStatus(ctx.root);
      return send(res, 200, { ok: true, pendingChanges: changes.length });
    }

    case '/api/commit': {
      if (!body.message || !String(body.message).trim()) return send(res, 400, { error: 'A commit message is required.' });
      const result = engine.commit(ctx.root, String(body.message).trim(), {
        allowDestructive: body.allowDestructive === true,
        author: 'dbgit-ui',
      });
      return send(res, 200, {
        commit: result.commit,
        migrationFile: result.migrationFile,
        sql: result.sql,
        skipped: result.skipped.map((item) => item.change.summary),
      });
    }

    case '/api/log':
      return send(res, 200, {
        commits: [...store.loadCommits(ctx.root)].reverse().map((commit) => ({
          ...commit,
          sql: store.readMigration(ctx.root, commit.migration),
        })),
      });

    case '/api/deploy/plan': {
      const plan = await engine.getDeployPlan(ctx.root, env(), {
        decisions: body.decisions || {},
        allowDestructive: body.allowDestructive === true,
        author: 'dbgit-ui',
      });
      return send(res, 200, plan);
    }

    case '/api/deploy': {
      const result = await engine.deploy(ctx.root, env(), {
        decisions: body.decisions || {},
        allowDestructive: body.allowDestructive === true,
        dryRun: body.dryRun === true,
        author: 'dbgit-ui',
      });
      return send(res, 200, result);
    }

    case '/api/pull': {
      const result = await engine.pull(ctx.root, env(), {
        plan: body.plan === true,
        decisions: body.decisions || {},
        all: body.all === true,
      });
      return send(res, 200, result);
    }

    case '/api/ledger': {
      const targetEnv = env();
      const commits = store.loadCommits(ctx.root);
      const history = await engine.withConnection(targetEnv, (conn) => readLedger(conn));
      return send(res, 200, {
        env: targetEnv.name,
        history,
        currentCommit: currentCommit(history),
        head: commits.length ? commits[commits.length - 1] : null,
        unknown: unknownCommits(commits, history),
      });
    }

    default:
      return send(res, 404, { error: `Unknown endpoint ${route}` });
  }
}

function summarize(snapshot) {
  return {
    schema: snapshot.schema,
    tables: Object.entries(snapshot.tables).map(([name, table]) => ({
      name,
      columnCount: Object.keys(table.columns).length,
      indexCount: Object.keys(table.indexes).length,
      primaryKey: table.primaryKey ? table.primaryKey.columns : [],
    })),
    views: Object.keys(snapshot.views).map((name) => ({ name })),
    sources: Object.values(snapshot.sources).map((source) => ({
      key: `${source.type}:${source.name}`,
      name: source.name,
      type: source.type,
      lines: (source.text || '').split('\n').length,
    })),
    sequences: Object.keys(snapshot.sequences).map((name) => ({ name })),
    triggers: Object.entries(snapshot.triggers).map(([name, trigger]) => ({ name, table: trigger.table, event: trigger.event })),
  };
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let data = '';
    req.on('data', (chunk) => {
      data += chunk;
      if (data.length > 5e6) reject(new Error('Request body too large.'));
    });
    req.on('end', () => {
      if (!data) return resolve({});
      try {
        resolve(JSON.parse(data));
      } catch {
        reject(new Error('Invalid JSON body.'));
      }
    });
    req.on('error', reject);
  });
}

function send(res, status, payload) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(payload));
}

module.exports = { startServer };
