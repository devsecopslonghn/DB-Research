'use strict';
const fs = require('fs');
const path = require('path');

const CONFIG_NAME = 'dbgit.config.json';
const STORE_DIR = '.dbgit';

function findRoot(startDir) {
  let dir = path.resolve(startDir);
  while (true) {
    if (fs.existsSync(path.join(dir, CONFIG_NAME))) return dir;
    const parent = path.dirname(dir);
    if (parent === dir) return null;
    dir = parent;
  }
}

function requireRoot(startDir = process.cwd()) {
  const root = findRoot(startDir);
  if (!root) {
    throw new Error(`No ${CONFIG_NAME} found here or in any parent directory. Run "dbgit init" first.`);
  }
  return root;
}

function loadConfig(root) {
  const file = path.join(root, CONFIG_NAME);
  const config = JSON.parse(fs.readFileSync(file, 'utf8'));
  if (!config.environments || Object.keys(config.environments).length === 0) {
    throw new Error(`${CONFIG_NAME} defines no environments.`);
  }
  return config;
}

function getEnv(config, name) {
  const envName = name || config.defaultEnv;
  if (!envName) {
    throw new Error('No environment given and no "defaultEnv" set in config.');
  }
  const env = config.environments[envName];
  if (!env) {
    const known = Object.keys(config.environments).join(', ');
    throw new Error(`Unknown environment "${envName}". Known environments: ${known}`);
  }
  return { name: envName, ...env };
}

function paths(root) {
  return {
    root,
    store: path.join(root, STORE_DIR),
    snapshots: path.join(root, STORE_DIR, 'snapshots'),
    head: path.join(root, STORE_DIR, 'HEAD'),
    commits: path.join(root, STORE_DIR, 'commits.json'),
    migrations: path.join(root, 'migrations'),
    config: path.join(root, CONFIG_NAME),
  };
}

module.exports = { CONFIG_NAME, STORE_DIR, findRoot, requireRoot, loadConfig, getEnv, paths };
