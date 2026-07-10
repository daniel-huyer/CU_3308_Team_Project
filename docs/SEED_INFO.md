# Seed Data Guide

This document explains how to use `seed.py` to populate the database with demo data.

---

## What the Seed Script Does

`seed.py` clears all existing data and repopulates the database with a known set of demo data including a test user, sample categories, transactions, and budgets. It is used to:

- Get a consistent starting state for local development
- Populate the csel.io database before a demo or presentation
- Reset your local database if data gets messy during testing

---

## When to Run It

- Before the Milestone 7 demo — run on csel.io to populate the demo database
- Any time your local database is in a broken or inconsistent state
- After pulling changes that include new migrations, to get fresh demo data

---

## How to Run It

### Prerequisites

Make sure your virtual environment is active and your `.env` file exists with correct values:

```bash
source .venv/bin/activate
source setup.cmds
```

Make sure the database schema is up to date:

```bash
flask db upgrade
```

### Run the seed script

```bash
python seed.py
```

You should see output like:

```
Clearing existing data...
Done.
Seeding users...
Created user: demo
Seeding complete.
Demo login -> username: demo  password: password123
```

---

## Demo Login Credentials

| Field | Value |
|---|---|
| Username | demo |
| Password | password123 |

---

## Adding Seed Data for New Models

As new models are built, uncomment the relevant sections in `seed.py` and add realistic sample data. Follow these guidelines:

- Use realistic amounts and dates — the demo should look like a real person's finances
- Include at least 2-3 months of transaction history so trend charts have data to display
- Make sure at least one budget category is over its limit so the alert feature is visible in the demo
- Keep the demo credentials simple — `demo` / `password123`

### Sections to uncomment as models are completed

| Section | Issue | Model |
|---|---|---|
| Categories | Issue 2.2 | `Category` |
| Transactions | Issue 2.3 | `Transaction` |
| Budgets | Issue 2.4 | `Budget` |

---

## Warning

The seed script **deletes all existing data** before inserting demo data. Never run it on a database with real user data. It is intended for development and demo purposes only.