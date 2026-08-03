// app/static/js/dashboard.js

async function fetchJSON(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Request to ${url} failed: ${res.status}`);
    return res.json();
}

function formatCurrency(n) {
    return `$${Number(n).toFixed(2)}`;
}

async function loadDashboard() {
    const page = document.getElementById('dashboard-page');
    const summaryUrl = page.dataset.summaryUrl;
    const transactionsUrl = page.dataset.transactionsUrl;

    const summaryRes = await fetchJSON(summaryUrl);
    const txRes = await fetchJSON(transactionsUrl);

    const summary = summaryRes.data;
    const transactions = txRes.data;

    document.getElementById('balance').textContent = formatCurrency(summary.balance);
    document.getElementById('income').textContent = formatCurrency(summary.income);
    document.getElementById('expenses').textContent = formatCurrency(summary.expenses);

    renderRecentTransactions(transactions.slice(0, 5));
}

function renderRecentTransactions(transactions) {
    const list = document.getElementById('recent-transactions');
    list.innerHTML = '';

    if (transactions.length === 0) {
        list.innerHTML = '<p class="muted">No transactions yet.</p>';
        return;
    }

    transactions.forEach(t => {
        const row = document.createElement('div');
        row.style.display = 'flex';
        row.style.justifyContent = 'space-between';
        row.style.padding = '0.5rem 0';

        const label = document.createElement('span');
        label.textContent = t.description || '(no description)';

        const amount = document.createElement('span');
        amount.className = t.type === 'income' ? 'amount-income' : 'amount-expense';
        const sign = t.type === 'income' ? '+' : '-';
        amount.textContent = `${sign}${formatCurrency(t.amount)}`;

        row.appendChild(label);
        row.appendChild(amount);
        list.appendChild(row);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    loadDashboard().catch(err => console.error('Failed to load dashboard:', err));
});
