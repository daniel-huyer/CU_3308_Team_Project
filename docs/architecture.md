# Application Architecture

## Overview

The Personal Finance Dashboard follows a standard flask web application architecture using the Model View Controller Pattern.

- **FrontEnd:** HTML templates, CSS, and Javascript provide the user interface.
- **Backend:** Flask handles HTTP request and applications logic.
- **Database:** SQLite stores user accounts, transactions, budgets and categories.

## Data Flow

1. The user enters information through a web form. (Ex: adding a transaction)
2. The request is sent to a flask route.
3. The flask route validates the data and interacts with the SQLAlchemy model.
4. SQLAlchemy reads from or writes to the SQLite database.
5. The data is returned to the flask route.
6. Flask renders an HTML template or returns a JSON response to the user.

## Data Flow Diagram

<img width="1440" height="900" alt="Data Flow Diagram" src="https://github.com/user-attachments/assets/a91cd343-be37-420f-8997-f747d1d48715" />

