# User Stories — JGT Personal Finance Dashboard
## Milestone 2

---

## Template

```
## User Story: <Title>

As a <role>
I want <action or feature>
So that <goal, benefit, or result>

**Actions to do:**

- <action 1>
- <action 2>
- <action 3>

---

As a <role>
I want <action or feature>
So that <goal, benefit, or result>

**Agreed Effort Level:** <team consensus value>

**Acceptance Criteria**

**Scenario:** <brief scenario name>

Given <starting context>
When <action or event>
Then <observable result>
And <additional observable result>

**Scenario:** <brief scenario name>

Given <starting context>
When <action or event>
Then <observable result>
And <additional observable result>
```

---
## Author: Daniel Huyer
### User Story 2: User Registration and Login

As a user
I want to create an account and log in
So that my financial data is private and accessible only to me.

**Actions to do:**

- Enter a username and password to register
- Log in with existing credentials
- Log out of the current session
- See an error message for invalid login attempts

>As a user  
>I want to create an account and log in  
>So that my financial data is private and accessible only to me.  
>
>**Agreed Effort Level:** 
>
>**Acceptance Criteria**
>
>**Scenario:** Successful registration
>
>Given the user is on the registration page  
>When the user enters a unique username and valid password and submits  
>Then a new account is created  
>And the user is redirected to the dashboard  
>
>**Scenario:** Duplicate username on registration  
>
>Given a username already exists in the system  
>When a new user attempts to register with the same username  
>Then the account is not created  
>And an error message indicates the username is already taken  
>
>**Scenario:** Successful login
>
>Given the user has a registered account  
>When the user enters correct credentials and submits  
>Then the user is authenticated and redirected to their dashboard  
>
>**Scenario:** Invalid login credentials
>
>Given the user enters an incorrect username or password  
>When the login form is submitted  
>Then access is denied  
>And an error message is displayed  
>
>**Scenario:** Logout
>
>Given the user is logged in   
>When the user clicks logout  
>Then the session is ended  
>And the user is redirected to the login page  

### User Story 2: Log Income

As a user
I want to record income
So that my dashboard reflects my full financial picture, not just my expenses.

**Actions to do:**

- Enter an income amount
- Select an income source (paycheck, freelance, gift, other)
- Select a date
- Save the income entry

>As a user  
>I want to record income  
>So that my dashboard reflects my full financial picture, not just my expenses.  
>
>**Agreed Effort Level:** 
>
>**Acceptance Criteria**
>
>**Scenario:** Successfully log income
>
>Given the user is logged in and on the income entry page  
>When the user enters a valid amount, selects an income source, selects a date, and saves  
>Then the income entry is stored in the database  
>And the dashboard total monthly income updates to reflect the new entry  
>
>**Scenario:** Missing required fields
>
>Given the user is on the income entry page  
>When the user attempts to save without entering an amount or selecting a source  
>Then the entry is not saved  
>And an error message indicates which fields are required  
>
>**Scenario:** Income entry appears in history
>
>Given the user has saved an income entry  
>When the user views their transaction history  
>Then the income entry is visible with the correct amount, source, and date  

### User Story 3: Delete or Edit a Transaction

As a user
I want to edit or delete a transaction I previously logged
So that I can correct mistakes without starting over.

**Actions to do:**

- Select an existing transaction
- Edit the amount, category, or date
- Save the updated transaction
- Delete a transaction and confirm removal

>As a user  
>I want to edit or delete a transaction I previously logged  
>So that I can correct mistakes without starting over.  
>
>**Agreed Effort Level:** 
>
>**Acceptance Criteria**
>
>**Scenario:** Edit a transaction
>
>Given the user has a previously logged transaction  
>When the user selects it, updates the amount, category, or date, and saves  
>Then the transaction is updated in the database  
>And the updated values are reflected in the transaction history and dashboard totals  
>
>**Scenario:** Delete a transaction
>
>Given the user has a previously logged transaction  
>When the user selects it and confirms deletion  
>Then the transaction is removed from the database  
>And the dashboard and history no longer include that transaction  
>
>**Scenario:** Cancel deletion
>
>Given the user selects a transaction and initiates deletion  
>When the user cancels the confirmation prompt  
>Then the transaction is not deleted  
>And no data is changed  

---
## Alejandro Banuelos Vielmas

### User Story 1: Record an Expense

As a user, I want to record an expense so that I can track where my money is being spent.

**Actions to do:**

- Enter the amount
- Select type of expense
- Save expense
- Update amount

### User Story 2: View Spending by Category

As a user, I want to view my spending by category so I can understand my habits.

**Actions to do:**

- Select type of expense category
- Select timeframe of spending

### User Story 3: Search Transactions

As a user, I want to search for transactions so that I can quickly find specific records.

**Actions to do:**

- Type in search bar what transaction to look for
- Select timeframe of transactions

---

## Kevin Bell

### User Story 1: Set a Monthly Budget

As a user, I want to set monthly spending limits for my expense categories so that I can manage
my budget and avoid overspending.

**Actions to do:**
- Select an expense category.
- Enter a monthly budget amount.
- Save the budget.
- Edit existing budgets.

### User Story 2: View Budget Status Dashboard

As a user, I want to view a dashboard summarizing my income, expenses, and budget status so
that I can understand my financial situation at a glance.

**Actions to do:**
- View total monthly income.
- View total monthly expenses.
- View category spending totals.
- View remaining budget amounts.
- View visual alerts for overspendin
