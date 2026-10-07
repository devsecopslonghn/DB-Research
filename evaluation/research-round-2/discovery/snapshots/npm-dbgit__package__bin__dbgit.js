#!/usr/bin/env node
'use strict';
const fs = require('fs');
const path = require('path');
const os = require('os');
const { CONFIG_NAME, requireRoot, loadConfig, getEnv } = require('../src/config');
const store = require('../src/store');
const engine = require('../src/engine');
const target = require('../src/target');
const { readLedger, currentCommit, unknownCommits } = require('../src/ledger');

const useColor = process.stdout.isTTY && process.env.NO_COLOR === undefined;
const CODES = { reset: '\x1b[0m', dim: '\x1b[2m', bold: '\x1b[1m', red: '\x1b[31m', green: '\x1b[32m', yellow: '\x1b[33m', blue: '\x1b[34m', cyan: '\x1b[36m' };
const paint = (color, text) => (useColor ? `${CODES[color]}${text}${CODES.reset}` : String(text));

function parseArgs(argv) {
  const positional = [];
  const flags = {};
  const repeated = { 'take-target': [], 'take-env': [] };

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '-m') {
      flags.message = argv[++i];
    } else if (arg.startsWith('--')) {
      const [key, inline] = arg.slice(2).split('=');
      const value = inline !== undefined ? inline : argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true;
      if (key in repeated) repeated[key].push(value);
      else flags[key] = value;
    } else {
      positional.push(arg);
    }
  }
  flags.takeTarget = repeated['take-target'];
  flags.takeEnv = repeated['take-env'];
  return { positional, flags };
}

function context(flags) {
  const root = requireRoot();
  const config = loadConfig(root);
  return { root, config, env: (name) => getEnv(config, name || flags.env) };
}

function decisionsFrom(flags) {
  const decisions = {};
  for (const locator of flags.takeTarget) decisions[locator] = 'take_target';
  for (const locator of flags.takeEnv) decisions[locator] = 'take_env';
  return decisions;
}

const commands = {
  async init(_positional, flags) {
    const root = process.cwd();
    const configFile = path.join(root, CONFIG_NAME);
    if (fs.existsSync(configFile) && flags.force !== true) {
      throw new Error(`${CONFIG_NAME} already exists here. Use --force to overwrite.`);
    }
    const schema = (flags.schema || 'MY_SCHEMA').toUpperCase();
    const template = {
      defaultEnv: 'local',
      environments: {
        local: {
          schema,
          user: flags.user || schema.toLowerCase(),
          password: flags.password || 'change-me',
          connectString: flags.connect || 'localhost:1521/ORCLPDB1',
        },
        test: { schema, user: schema.toLowerCase(), password: 'env:DBGIT_TEST_PASSWORD', connectString: 'test-host:1521/orcl' },
        uat: { schema, user: schema.toLowerCase(), password: 'env:DBGIT_UAT_PASSWORD', connectString: 'uat-host:1521/erp' },
      },
    };
    fs.writeFileSync(configFile, JSON.stringify(template, null, 2) + '\n');
    store.ensureStore(root);

    console.log(`Created ${paint('cyan', CONFIG_NAME)}\n`);
    console.log('Passwords for shared environments should be written as "env:VAR_NAME"');
    console.log('so real credentials stay out of the repository.\n');
    console.log('Next:');
    console.log(`  1. edit ${CONFIG_NAME} to point at your databases`);
    console.log(`  2. ${paint('bold', 'dbgit baseline')}   capture the current schema as the starting point`);
    console.log(`  3. ${paint('bold', 'dbgit ui')}         open the visual editor`);
  },

  async baseline(_positional, flags) {
    const { root, env } = context(flags);
    const target_ = env();
    const { commit, snapshot } = await engine.baseline(root, target_, { force: flags.force === true });
    const counts = {
      tables: Object.keys(snapshot.tables).length,
      views: Object.keys(snapshot.views).length,
      programs: Object.keys(snapshot.sources).length,
      sequences: Object.keys(snapshot.sequences).length,
      triggers: Object.keys(snapshot.triggers).length,
    };
    console.log(paint('green', `Baseline captured from ${target_.name} (${snapshot.schema}).`));
    console.log(`  ${counts.tables} tables, ${counts.views} views, ${counts.programs} program units, ${counts.sequences} sequences, ${counts.triggers} triggers`);
    console.log(`  written to ${paint('cyan', 'schema/')} as commit ${commit.id}`);
    console.log(`\nEdit the schema with ${paint('bold', 'dbgit ui')}, then deploy it with ${paint('bold', 'dbgit deploy --env <name>')}.`);
  },

  async status(_positional, flags) {
    const { root } = context(flags);
    const { changes, head } = engine.getStatus(root);
    console.log(`Target schema, last commit ${head ? paint('bold', `${head.id} ${head.message}`) : paint('yellow', 'none')}\n`);
    if (changes.length === 0) {
      console.log(paint('green', 'No changes. The target schema matches the last commit.'));
      return;
    }
    printChanges(changes);
    console.log(`\n${changes.length} change(s). Save them with  ${paint('bold', 'dbgit commit -m "what changed"')}`);
  },

  async diff(_positional, flags) {
    const { root } = context(flags);
    const { changes, desired } = engine.getStatus(root);
    if (changes.length === 0) {
      console.log(paint('green', 'No changes.'));
      return;
    }
    const { sql } = engine.buildMigrationSql(changes, { allowDestructive: flags['allow-destructive'] === true }, {
      commitId: '(uncommitted)',
      message: 'uncommitted changes',
      createdAt: new Date().toISOString(),
      author: os.userInfo().username,
      schema: desired.schema,
    });
    console.log(sql);
  },

  async commit(_positional, flags) {
    const { root } = context(flags);
    const message = flags.message;
    if (!message || message === true) throw new Error('A commit message is required:  dbgit commit -m "what changed"');

    const result = engine.commit(root, String(message), { allowDestructive: flags['allow-destructive'] === true });
    console.log(paint('green', `Committed ${result.commit.id}: ${result.commit.message}`));
    console.log(`  ${result.commit.changeCount} change(s) -> ${paint('cyan', `migrations/${result.migrationFile}`)}`);
    for (const change of result.commit.changes) {
      console.log(`    ${change.destructive ? paint('red', '!') : ' '} ${change.summary}`);
    }
    if (result.skipped.length > 0) {
      console.log(paint('yellow', `\n  ${result.skipped.length} destructive change(s) were recorded but no SQL was generated for them.`));
      console.log(`  Re-run with ${paint('bold', '--allow-destructive')} to include them.`);
    }
  },

  async log(_positional, flags) {
    const { root } = context(flags);
    const commits = store.loadCommits(root);
    if (commits.length === 0) {
      console.log('No commits yet. Run "dbgit baseline" to start.');
      return;
    }
    for (const commit of [...commits].reverse()) {
      console.log(`${paint('yellow', commit.id)}  ${paint('bold', commit.message)}`);
      console.log(`  ${paint('dim', `${commit.createdAt}  ${commit.author}  ${commit.migration}`)}`);
      if (flags.verbose === true) for (const change of commit.changes) console.log(`    ${change.summary}`);
      console.log('');
    }
  },

  async deploy(_positional, flags) {
    const { root, env } = context(flags);
    const targetEnv = env();
    const dryRun = flags['dry-run'] === true;
    const decisions = decisionsFrom(flags);

    const plan = await engine.getDeployPlan(root, targetEnv, {
      decisions,
      allowDestructive: flags['allow-destructive'] === true,
    });

    console.log(`Deploying to ${paint('cyan', plan.env)} (${plan.schema})`);
    console.log(`  target at commit ${paint('bold', (plan.headCommit || {}).id || 'none')}, environment last deployed ${plan.currentCommit ? paint('bold', plan.currentCommit) : paint('yellow', 'never')}\n`);

    const undecided = plan.conflicts.filter((conflict) => !decisions[conflict.locator]);
    if (undecided.length > 0) {
      console.log(paint('yellow', `${undecided.length} difference(s) need a decision:\n`));
      for (const conflict of undecided) {
        printConflict(conflict);
      }
      console.log(paint('dim', '  Choose per item and re-run, for example:'));
      console.log(paint('dim', `    dbgit deploy --env ${plan.env} --take-env ${undecided[0].locator}`));
      console.log(paint('dim', `    dbgit deploy --env ${plan.env} --take-target ${undecided[0].locator}`));
      console.log(paint('dim', '  Anything left undecided is skipped and neither side is changed.\n'));
    }

    if (plan.changes.length === 0) {
      console.log(
        undecided.length > 0
          ? paint('yellow', 'Nothing to run — every difference above is still undecided.')
          : paint('green', `${plan.env} already matches the target schema.`)
      );
      return;
    }

    if (dryRun) {
      console.log(paint('blue', `Would run ${plan.statements.filter((s) => !s.skipped).length} statement(s):\n`));
      for (const statement of plan.statements) {
        if (statement.skipped) console.log(paint('yellow', indent(statement.sql)));
        else console.log(`  ${paint('dim', statement.summary)}\n${indent(statement.sql)};\n`);
      }
      console.log(paint('yellow', 'Dry run — nothing was applied.'));
      return;
    }

    const result = await engine.deploy(root, targetEnv, {
      decisions,
      allowDestructive: flags['allow-destructive'] === true,
    });
    for (const item of result.results) {
      const label = item.status === 'ok' ? paint('green', 'ok    ') : paint('red', 'FAILED');
      console.log(`${label}  ${item.summary}`);
      if (item.error) console.log(paint('red', `        ${item.error}`));
    }
    if (result.adopted && result.adopted.length) {
      console.log(paint('cyan', `\n  Adopted into the target schema: ${result.adopted.join(', ')}`));
      console.log('  Commit the updated schema/ files to record this.');
    }
    if (result.skipped.length) {
      console.log(paint('yellow', `\n  ${result.skipped.length} destructive change(s) were not applied. Re-run with --allow-destructive to include them.`));
    }
    if (result.failed) process.exitCode = 1;
    else if (result.skipped.length || undecided.length) {
      console.log(paint('yellow', `\n${plan.env} is partly updated — ${result.skipped.length} destructive and ${undecided.length} undecided change(s) remain.`));
    } else {
      console.log(paint('green', `\n${plan.env} is now at the target schema.`));
    }
  },

  async pull(_positional, flags) {
    const { root, env } = context(flags);
    const targetEnv = env();
    const decisions = decisionsFrom(flags);
    const takeAll = flags.all === true;

    const preview = await engine.pull(root, targetEnv, { plan: true });
    if (preview.candidates.length === 0) {
      console.log(paint('green', `Nothing to pull — ${targetEnv.name} matches the target schema.`));
      return;
    }
    if (!takeAll && Object.keys(decisions).length === 0) {
      console.log(`${preview.candidates.length} difference(s) found in ${paint('cyan', targetEnv.name)}:\n`);
      for (const candidate of preview.candidates) printConflict(candidate);
      console.log(paint('dim', '  Bring one across:'));
      console.log(paint('dim', `    dbgit pull --env ${targetEnv.name} --take-env ${preview.candidates[0].locator}`));
      console.log(paint('dim', `  Or bring all of them across:  dbgit pull --env ${targetEnv.name} --all\n`));
      return;
    }

    const result = await engine.pull(root, targetEnv, { decisions, all: takeAll });
    if (result.adopted.length === 0) {
      console.log('Nothing adopted.');
      return;
    }
    console.log(paint('green', `Adopted ${result.adopted.length} change(s) into the target schema:`));
    for (const locator of result.adopted) console.log(`  ${locator}`);
    console.log(`\nReview with ${paint('bold', 'dbgit status')}, then ${paint('bold', 'dbgit commit -m "..."')}`);
  },

  async ledger(_positional, flags) {
    const { root, env } = context(flags);
    const targetEnv = env();
    const commits = store.loadCommits(root);
    const history = await engine.withConnection(targetEnv, (conn) => readLedger(conn));

    console.log(`${paint('cyan', targetEnv.name)} (${targetEnv.schema})\n`);
    if (history.length === 0) {
      console.log('  no deploys recorded');
    } else {
      for (const entry of history) {
        console.log(`  ${paint('green', entry.appliedAt)}  commit ${paint('bold', entry.commitId)}  ${entry.message || ''}`);
        console.log(`  ${paint('dim', `    ${entry.statementCount} statement(s) by ${entry.appliedBy}`)}`);
      }
    }
    const current = currentCommit(history);
    const head = commits.length ? commits[commits.length - 1] : null;
    console.log(`\n  environment at ${paint('bold', current || 'none')}, repository head ${paint('bold', head ? head.id : 'none')}`);
    if (head && current !== head.id) console.log(paint('yellow', `  ${targetEnv.name} is behind. Run: dbgit deploy --env ${targetEnv.name} --dry-run`));

    const unknown = unknownCommits(commits, history);
    if (unknown.length) {
      console.log(paint('red', `\n  ${unknown.length} deploy(s) reference commits that are not in this repository:`));
      for (const entry of unknown) console.log(`    ${entry.commitId}  ${entry.message || ''}  ${paint('dim', entry.appliedAt)}`);
      console.log(paint('dim', '  Someone deployed from a different branch or checkout.'));
    }
  },

  async ui(_positional, flags) {
    const { root, config } = context(flags);
    if (!target.exists(root)) throw new Error('No schema/ folder yet. Run "dbgit baseline" first.');
    const { startServer } = require('../src/ui/server');
    await startServer({ root, config, port: Number(flags.port || 5757), open: flags.open !== false });
  },

  async help() {
    console.log(`
${paint('bold', 'dbgit')} — version control for a database schema

  ${paint('bold', 'dbgit init')}                    create dbgit.config.json here
  ${paint('bold', 'dbgit baseline')}                capture an existing database as the starting point
  ${paint('bold', 'dbgit ui')}                      open the visual schema editor      ${paint('dim', '--port 5757')}

  ${paint('bold', 'dbgit status')}                  what changed in the target schema
  ${paint('bold', 'dbgit diff')}                    the SQL for those changes
  ${paint('bold', 'dbgit commit -m "..."')}         save the changes and write a migration
  ${paint('bold', 'dbgit log')}                     commit history                     ${paint('dim', '--verbose')}

  ${paint('bold', 'dbgit deploy --env test')}       bring an environment to the target ${paint('dim', '--dry-run')}
  ${paint('bold', 'dbgit pull --env local')}        bring database changes back into the target
  ${paint('bold', 'dbgit ledger --env test')}       what an environment has had deployed

Resolving differences (both deploy and pull):
  --take-target <locator>    use the target schema's version
  --take-env <locator>       use the environment's version, and adopt it into schema/
  ${paint('dim', 'Anything left undecided is skipped: neither side changes.')}

Other flags:
  --env <name>               which environment to use (default: config defaultEnv)
  --allow-destructive        also generate drops and narrowing changes
`);
  },
};

function printChanges(changes) {
  const groups = {};
  for (const change of changes) {
    const group = change.table || { view: 'views', source: 'program units', sequence: 'sequences', trigger: 'triggers' }[change.kind.split('.')[0]] || 'other';
    (groups[group] = groups[group] || []).push(change);
  }
  for (const [group, items] of Object.entries(groups)) {
    console.log(paint('bold', `  ${group}`));
    for (const change of items) {
      console.log(`    ${change.destructive ? paint('red', '!') : paint('green', '+')} ${change.summary}`);
    }
  }
}

function printConflict(conflict) {
  const heading = conflict.action === 'missing_in_target' ? paint('yellow', 'only in the environment') : conflict.action === 'missing_in_env' ? paint('blue', 'only in the target') : paint('red', 'differs');
  console.log(`  ${paint('bold', conflict.locator)}   ${heading}`);
  if (conflict.targetText) console.log(`    target       ${conflict.targetText.split('\n')[0]}`);
  if (conflict.envText) console.log(`    ${conflict.envName.padEnd(12)} ${conflict.envText.split('\n')[0]}`);
  console.log('');
}

const indent = (text) => String(text).split('\n').map((line) => `    ${line}`).join('\n');

(async () => {
  const { positional, flags } = parseArgs(process.argv.slice(2));
  const name = positional[0] || 'help';
  const command = commands[name];
  if (!command) {
    console.error(paint('red', `Unknown command "${name}".`));
    await commands.help();
    process.exitCode = 1;
    return;
  }
  try {
    await command(positional.slice(1), flags);
  } catch (error) {
    console.error(paint('red', `\n${error.message}\n`));
    if (flags.debug === true) console.error(error.stack);
    process.exitCode = 1;
  }
})();
