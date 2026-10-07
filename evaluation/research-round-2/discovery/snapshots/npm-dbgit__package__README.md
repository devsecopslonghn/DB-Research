# dbgit

Version control for a database schema.

You keep a **target schema** in your repository — plain files describing what the
database is supposed to look like. You edit it, commit it, and deploy it to any
environment. When an environment has drifted, dbgit shows you both sides and
asks which one wins, the way a merge conflict does.

Currently supports Oracle. Connects in thin mode, so there is no Oracle Instant
Client to install.

```
npm install -g @lovelytoonz/dbgit
```

The command is `dbgit` once installed.

## Why

Migration tools like Flyway replay scripts you wrote by hand. That works until
you have altered a local database at 2am and cannot remember what you changed,
or until five environments have quietly diverged from each other and from the
repository.

dbgit works from the schema itself:

- **`dbgit status`** answers "what did I change?" without you having to remember.
- **`dbgit deploy`** computes SQL against the environment's *actual* state, so an
  environment that is already half up to date only gets the statements it needs.
- **`dbgit pull`** brings changes made directly in a database back into the repo.
- Conflicts are surfaced and resolved explicitly, never silently overwritten.

## Getting started

```bash
cd your-project
dbgit init --schema APP_DEV        # writes dbgit.config.json
# edit dbgit.config.json to point at your databases
dbgit baseline                     # capture the current schema into schema/
dbgit ui                           # visual editor at http://127.0.0.1:5757
```

`baseline` reads an existing database and writes `schema/`. Nothing is created or
dropped — it records what is already there as the starting point.

## Configuration

```json
{
  "defaultEnv": "local",
  "environments": {
    "local": {
      "schema": "APP_DEV",
      "user": "app_dev",
      "password": "app_dev",
      "connectString": "localhost:1521/ORCLPDB1"
    },
    "uat": {
      "schema": "APP_UAT",
      "user": "app_uat",
      "password": "env:DBGIT_UAT_PASSWORD",
      "connectString": "uat-db.internal:1521/orcl"
    }
  }
}
```

Write shared-environment passwords as `env:VAR_NAME` so real credentials are read
from the environment instead of being committed.

## What lives in the repository

```
dbgit.config.json          environments
schema/                    the target schema — review this in merge requests
  tables/ORDERS.json
  views/V_ORDER_SUMMARY.sql
  programs/procedures/PROCESS_ORDER_PRC.sql
migrations/                SQL written for you at commit time
  V20260721143002__add_remark.sql
.dbgit/                    commit history and snapshots
```

Tables are JSON because their structure is what matters. Views, packages,
procedures and triggers stay as `.sql` because they already are source code.

```json
{
  "name": "ORDERS",
  "columns": {
    "ORDER_ID": { "type": "NUMBER(12)", "notNull": true },
    "AMT":        { "type": "NUMBER(18,2)", "default": "0" },
    "REMARK":     { "type": "VARCHAR2(500 CHAR)" }
  },
  "primaryKey": { "name": "PK_ORDERS", "columns": ["ORDER_ID"] },
  "indexes": { "IX_ORDERS_CUSTOMER": { "columns": ["CUSTOMER_ID"] } }
}
```

## A normal day

Add a column in the UI, or by editing the JSON. Nothing has touched a database
yet — only the file changed.

```bash
dbgit status
#   ORDERS
#     + added column ORDERS.REMARK VARCHAR2(500 CHAR) NULL

dbgit deploy --env local --dry-run   # see the SQL
dbgit deploy --env local             # try it against your own database

dbgit commit -m "add a remark to orders"
#   Committed 0007 -> migrations/V20260721143002__add_a_remark_to_orders.sql

git add schema migrations .dbgit && git commit    # ships with the application code
```

Later, on a shared environment:

```bash
dbgit deploy --env uat --dry-run
```

## Resolving differences

When an environment does not match, dbgit works out whether *you* changed
something or the *environment* did, by comparing both against the commit that
environment was last deployed to.

```
column:ORDERS.AMT   differs
  target       NUMBER(18,2) NOT NULL
  uat          NUMBER(16,2) NULL

column:ORDERS.BRANCH_CODE   only in the environment
  uat          VARCHAR2(10 CHAR) NULL
```

Decide per item:

```bash
dbgit deploy --env uat --take-target column:ORDERS.AMT \
             --take-env    column:ORDERS.BRANCH_CODE
```

- `--take-target` pushes your version to the environment.
- `--take-env` adopts the environment's version into `schema/`, ready to commit.
- Anything you do not decide is **skipped** — neither side changes, and you are
  asked again next time.

## Recovering an ALTER you ran by hand

```bash
dbgit pull --env local        # list what the database has that the repo does not
dbgit pull --env local --all  # bring it all into schema/
dbgit status
dbgit commit -m "..."
```

## Destructive changes

Dropping a column or table, and narrowing a type, are never generated unless you
ask:

```bash
dbgit deploy --env uat --allow-destructive
```

Without the flag they are still reported, so you can see them — they just are not
turned into SQL.

## Deploy history

Each environment carries a `DBGIT_CHANGELOG` table recording every deploy.

```bash
dbgit ledger --env uat
```

It also flags deploys made from a branch or checkout you do not have.

## Commands

| | |
|---|---|
| `dbgit init` | create `dbgit.config.json` |
| `dbgit baseline` | capture an existing database as the starting point |
| `dbgit ui` | visual schema editor (`--port`) |
| `dbgit status` | what changed in the target schema |
| `dbgit diff` | the SQL for those changes |
| `dbgit commit -m "..."` | save changes and write a migration |
| `dbgit log` | commit history (`--verbose`) |
| `dbgit deploy --env <name>` | bring an environment to the target (`--dry-run`) |
| `dbgit pull --env <name>` | bring database changes back into the target |
| `dbgit ledger --env <name>` | what an environment has had deployed |

## Notes

- The UI binds to `127.0.0.1` only. It can change schemas and deploy, so it is
  deliberately not reachable from the network.
- Oracle commits DDL implicitly. If a deploy fails partway, earlier statements
  stay applied; dbgit stops there and the next deploy recomputes from the
  environment's real state.
- Sequence `LAST_NUMBER` and object timestamps are excluded from snapshots, so
  ordinary use does not show up as schema drift.

## Requirements

Node 18 or newer.

## License

MIT
