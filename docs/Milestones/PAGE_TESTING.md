## 1. Login / Register Page

### Page Description
Allows users to log in to an existing JGT Finance account or create a new account.

Mockup: `docs/wireframes/login-web-version.png`

### Parameters Needed
- `email_or_username`
- `password`
- Login/register mode

### Data Needed to Render the Page
- App name/logo
- Form labels and placeholders
- Authentication error/success messages
- User account data for login validation

### Link Destinations
- **Log In**: authenticates user and redirects to Dashboard
- **Create Account**: opens registration flow
- **Forgot password?**: opens password reset flow
- **Already have an account? Log in**: returns to login mode

### Rendering Tests
- App name/logo visible
- Email/username and password render
- Log In and Create Account buttons render
- Forgot password link renders
- Empty or invalid login shows an error
- Valid login redirects to Dashboard
- Page layout is centered and readable


## 2. Dashboard Page

### Page Description
Displays a summary of the user’s financial information, including current balance, income, expenses, spending trends, recent transactions, and spending by category.

Mockup: `docs/wireframes/dashboard-web-version.png`

### Parameters Needed
- User account ID/session
- Income transactions
- Expense transactions
- Transaction categories
- Transaction amounts and dates

### Data Needed to Render the Page
- Current account balance
- Individual transaction data
- Transaction type: income or expense
- Transaction category
- Transaction amount
- Recent transactions
- Spending trend data over time

### Link Destinations
- **+ Add Transaction**: goes to Add Transaction page
- **Settings**: goes to Settings page
- Sidebar links: Home, History, Add Transaction, Budget, Savings Goals, Settings

### Rendering Tests
- Check that the current balance shows on the page
- Check that income and expense totals show on the page
- Check that recent transactions show in the list
- Check that the spending trend chart appears
- Check that the category circle chart appears
- Add an income transaction and check that the balance goes up
- Add an expense transaction and check that the balance goes down
- Check that transaction categories show up in the circle chart
- Check that the Add Transaction button goes to the Add Transaction page
- Check that the sidebar links go to the correct pages


## 3. Add Transaction Page

### Page Description
Allows users to add a new expense or income transaction. The user enters the amount, category, date, and description. This transaction is then used in the dashboard summary and transaction history.

Mockup: `docs/wireframes/add-transaction-web-version.png`

### Parameters Needed
- Transaction type: expense or income
- Amount
- Category
- Date
- Description/notes

### Data Needed to Render the Page
- List of transaction categories
- User account/session
- Current balance
- Existing transaction data

### Link Destinations
- **Save Transaction**: saves the transaction and updates Dashboard and Transaction History
- **Cancel**: returns to Dashboard or previous page
- Sidebar links: Home/Dashboard, Transaction History, Add Transaction, Budget, Savings Goals, Settings

### Rendering Tests
- Check that the expense/income selector appears and works
- Check that amount, category, date, and description fields appear
- Check that the Save Transaction button appears
- Check that the Cancel link appears
- Enter an expense and check that it appears on Transaction History
- Enter an income and check that it appears on Transaction History
- Check that the Dashboard balance updates after saving
- Check that the transaction category contributes to the Dashboard category chart
- Check that missing required fields show an error



## 4. Transaction History Page

### Page Description
Shows all past income and expense transactions. Each transaction includes the date, description, category, and amount. Users can search transactions by description and filter by category or date.

Mockup: `docs/wireframes/transaction-history-web-version.png`

### Parameters Needed
- User account/session
- Search text
- Category filter
- Date filter/date range

### Data Needed to Render the Page
- List of transactions
- Transaction date
- Transaction description
- Transaction category
- Transaction amount
- Transaction type: income or expense
- Category list, including misc.

### Link Destinations
- Sidebar links: Home/Dashboard, Transaction History, Add Transaction, Budget, Savings Goals, Settings

### Rendering Tests
- Check that the transaction table appears
- Check that date, description, category, and amount columns appear
- Check that transactions added from the Add Transaction page show up here
- Check that income and expenses are shown correctly
- Check that the search bar filters transactions by description (aka name)
- Check that the category filter works
- Check that miscellaneous category transactions can appear
- Check that the date filter/date range works
- Check that dates display in the correct format
- Check that the sidebar links go to the correct pages



## 5. Budget Settings Page

### Page Description
Allows users to enter monthly expenses, savings goals, and debt payments/recurring bills. The page uses this information to estimate an ideal yearly salary and monthly take-home income.

Mockup: `docs/wireframes/budget-settings-web-version.png`

### Parameters Needed
- User account/session
- Current monthly expenses
- Monthly savings goal
- Debt payments/recurring obligations

### Data Needed to Render the Page
- Expense totals from transaction data
- User-entered savings goal
- User-entered debt/obligation amount
- Calculated ideal salary
- Estimated monthly take-home income

### Link Destinations
- **Calculate Ideal Salary**: updates the suggested salary result
- Sidebar links: Home/Dashboard, Transaction History, Add Transaction, Budget, Savings Goals, Settings

### Rendering Tests
- Check that monthly expenses, savings goal, and debt payment fields appear
- Check that the Calculate Ideal Salary button appears
- Check that the suggested ideal salary box appears
- Enter monthly expenses and check that they are used in the calculation
- Enter a savings goal and check that it changes the result
- Enter debt/recurring payments and check that they change the result
- Check that invalid or empty inputs show an error or default value
- Check that sidebar links go to the correct pages