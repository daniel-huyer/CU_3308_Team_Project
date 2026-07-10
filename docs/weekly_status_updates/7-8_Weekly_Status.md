# 7-8_WEEKLY_STATUS.md

## Project Milestone 3: Weekly Status Report

**Project:** JGT Finance  
**Team Number:** 4  
**Team Name:** JGT Finance

---

## Reporting Period

**Week:** 4  
**Meeting Held:** Yes  
**Meeting Date:** July 8th, 2026  
**Meeting Duration:** 30 minutes  
**Meeting Format:** Microsoft Teams

---

## Overview

This document captures the **weekly status** of the JGT Finance project for the specified reporting period.  
It is intended to provide a concise snapshot of progress, plans, and risks, and will be updated weekly throughout the project.

This weekly status format is designed to:

- Track ongoing progress over time
- Surface risks and blockers early
- Provide accountability for individual contributions
- Supplement the project management tool used by the team

---

## Project Management Snapshot

The team is using a shared **GitHub Projects Board** to manage tasks and sprint progress.  
At the time of this report:

- Columns include: Todo, In Progress, Done, Backlog
- Tasks are assigned to individual team members
- Due dates and priorities are tracked per task

<img width="1440" height="693" alt="Screenshot 2026-07-09 at 8 31 25 PM" src="images/7-30_project_mgmt_snapshot.png" />

---

## Progress Since Last Week

This week the team focused on **Flask application setup, database configuration, and project infrastructure**. The core application structure is now running on both local machines and the csel.io virtual environment.

Key accomplishments include:

- Flask application factory pattern implemented and running on csel.io via JupyterHub proxy
- SQLite database configured with Flask-SQLAlchemy and Flask-Migrate
- User model created with initial migration applied
- Blueprint routing established with base template and dashboard page rendering
- Branch protection rules configured on main (2 required approvals)
- GitHub Milestones created and issues assigned per Epic

---

## Completed Tasks

- Initialized repository structure with correct Flask directory layout
- Configured Flask app factory pattern with `create_app()` in `app/__init__.py`
- Set up csel.io proxy support via `prefix.py` middleware
- Created `app/db.py` with SQLAlchemy instance and wired into factory
- Defined User model in `app/models.py`
- Generated and applied initial database migration for users table
- Created `base.html` shared layout and `dashboard.html` template
- Added Blueprint routing via `app/routes.py`
- Created `seed.py` for demo data population
- Wrote `RUN_SETUP.md` and `SEED_INFO.md` developer documentation
- Merged Milestone 1 branches into main

---

## Planned Tasks for Next Week

- Implement user registration and login (Milestone 3 — Authentication)
- Build remaining database models: Category, Transaction, Budget
- Generate migrations for new models
- Begin frontend pages for transaction entry and budget settings

---

## Blockers and Issues

- Significant time spent resolving csel.io proxy URL routing — resolved by setting `FLASK_APP=prefix.py` and reading `JUPYTERHUB_SERVICE_PREFIX` at request time rather than app startup
- Merge conflicts between `chore/setup-flask` and `chore/db-setup` on `__init__.py` and `requirements.txt` — resolved during integration

---

## Risks and Mitigation

**Identified Risk:** Integration conflicts between parallel branches

- _Mitigation:_ Established PR review process with 2 required approvals and a defined merge order (setup before db-setup). Will continue merging main into feature branches before opening PRs.

---

## Individual Contributions This Week

- **Daniel Huyer:** Flask app factory setup, csel.io proxy integration, blueprint routing, base/dashboard templates, seed script, developer documentation, branch protection rules, GitHub Milestones setup
- **Kevin Bell:** SQLite database configuration with SQLAlchemy, Flask-Migrate setup, initial database migration for users table
- **Bri Rowe:** UI wireframes for core application pages (dashboard, login, add transaction, budget settings, transaction history)
- **Alejandro Banuelos Vielmas:** Repository initialization and directory structure, application data flow documentation and architecture notes

---

## Notes

This file will be updated weekly as the project progresses.  
Earlier weekly entries may be retained below or moved to an archive directory if the file grows large.