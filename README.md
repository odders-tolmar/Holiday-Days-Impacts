# SQL Explore — Setup Guide

A template for querying an Azure Synapse Serverless SQL database using Python, SQLAlchemy, pandas, and Jupyter Notebook in VS Code.

---

## Prerequisites

- Python — https://www.python.org/downloads/
- Git — https://git-scm.com/downloads/
- VS Code — https://code.visualstudio.com/
- VS Code Extensions: Python (Microsoft), Jupyter (Microsoft), Claude (Anthropic)
- Microsoft ODBC Driver 18 for SQL Server — https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
- A GitHub account
- Azure Synapse SQL credentials

---

> **Heads up:** Steps 1 and 2 are manual setup steps you perform in the GitHub and VS Code UIs. Once your project is cloned locally, the remaining steps run from the VS Code terminal — or you can hand them off to Claude using the bootstrap prompt below.

---

## Step 1: Create a new repo from the template *(manual — GitHub UI)*
*Gives you a private copy of the template with all the boilerplate already wired up, so you start with a working project instead of an empty repo.*

1. Go to the [sql-explore-template](https://github.com/mfletcher1541/sql-explore-template) repo on GitHub and click the green **"Use this template"** button → **"Create a new repository"**.
2. Fill out the new repo details:
   - Set **Owner** and **repo name**
   - Select **Private**
   - Leave **"Include all branches"** unchecked
3. Click **"Create repository"**. Leave this tab open — you'll come back to it.

---

## Step 2: Clone your new repo in VS Code *(manual — VS Code UI)*
*Pulls the project onto your machine and connects it to your new repo (not the template) so future pushes go to the right place.*

1. Open VS Code and click the **Source Control** icon in the left sidebar.
2. Click **"Clone Repository"** — a search box will appear at the top with a list of your GitHub repos.
3. Type the name of your new repo, select it from the list, then pick a local folder to save it in.
4. Click **"Open"** when prompted.

To verify it's connected correctly, open VS Code's terminal and run:

```bash
git remote -v
```

You should see your new repo name in the URL, not the template's.

---

## Step 3: Bootstrap the rest of setup with Claude
*Hand off the rest of the setup — virtual environment, dependencies, credentials, connection test, schema extraction, and Jupyter kernel — to Claude instead of running each step yourself.*

> **First-time note:** Claude will prompt for permission before running each command (Python, pip, file writes). Approve them as they come up — they're the same commands listed in Steps 4–9 below.

Open the Claude panel in VS Code, **replace the placeholder values below with your real credentials**, then paste the prompt:

```
This project is a template for SQL exploration. Read README.md and
assume I have already completed steps 1 and 2 (created the repo from
the template and cloned it in VS Code).

Please run steps 4-9 for me. Use these connection details when you
create the .env file in step 5:

DB_SERVER=<your-server>.sql.azuresynapse.net
DB_NAME=<your-database-name>
DB_DRIVER=ODBC Driver 18 for SQL Server
DB_USER=<your-username>
DB_PASSWORD=<your-password>

Verify each step succeeded before moving to the next, and stop and ask
me if anything fails. Once setup is complete, help me start exploring
the database.
```

If you'd rather run the steps yourself, just continue below.

---

## Step 4: Create your virtual environment and install dependencies
*Isolates this project's Python packages so they don't collide with other projects or your system Python.*

In the VS Code terminal (PowerShell is the default on Windows):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> **If you see `running scripts is disabled on this system`**, run this once to allow signed scripts for your user account, then retry the activate step:
>
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```

---

## Step 5: Configure credentials
*`db.py` reads your connection details from `.env`. The file is gitignored, so your credentials never end up in source control.*

Copy `.env.example` to `.env` and fill in your database details:

```
DB_SERVER=your-server.sql.azuresynapse.net
DB_NAME=your_database
DB_DRIVER=ODBC Driver 18 for SQL Server
DB_USER=your_username
DB_PASSWORD=your_password
```

---

## Step 6: Test your connection
*Confirms your credentials, ODBC driver, and network access are all working before you start writing queries.*

```bash
python db.py
```

You should see your Azure Synapse version printed.

---

## Step 7: Extract your schema
*Generates `schema.sql` so you — and Claude — can reference real table and column names instead of guessing. Re-run whenever your schema changes.*

```bash
python extract_schema.py
```

This creates `schema.sql` with all your table and column definitions.

---

## Step 8: Register the Jupyter kernel
*Tells Jupyter to use this project's `.venv` so notebooks run with the right dependencies.*

```bash
python -m ipykernel install --user --name=sql-explore --display-name "SQL Explore"
```

---

## Step 9: Start querying
*You're set up — open the notebook and run a query against your database.*

1. Open `query.ipynb` in VS Code
2. Click **Select Kernel** → **Python Environments** → **SQL Explore**
3. Replace `your_table_name` with a table from `schema.sql` and run

---

## Starting a Claude session later

If Claude is already running from the bootstrap in Step 3, you can skip this section. Use it when you come back to the project in a fresh Claude session (or if you ran setup manually and want to start querying with Claude's help).

Open the Claude panel in VS Code with `schema.sql` and `query.ipynb` open, then paste the following to start a session:

```
I am working with an Azure Synapse serverless SQL database using the SQL Explore template.

The project is set up as follows:
- db.py — SQLAlchemy + pyodbc connection engine, reads credentials from .env
- extract_schema.py — generates schema.sql with all table and column definitions
- query.ipynb — Jupyter notebook using pd.read_sql(sql, engine) for querying
- schema.sql — all table and column definitions for this database

Please reference schema.sql for all table and column names when helping me write queries.
You can also run queries directly using the Bash tool with the project's .venv Python environment.
```

Claude can now write and run queries directly against your database.

---

## Project structure

```
your-project/
├── .venv/               ← isolated Python environment (never commit)
├── .env                 ← your credentials (never commit)
├── .env.example         ← credential template
├── .gitignore
├── db.py                ← database connection engine
├── extract_schema.py    ← run to generate schema.sql
├── schema.sql           ← table definitions (gitignored by default)
├── query.ipynb          ← Jupyter notebook for queries
└── requirements.txt     ← direct dependencies
```
