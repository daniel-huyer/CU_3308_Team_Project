// app/static/js/dashboard.js

async function fetchJSON(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Request to ${url} failed: ${res.status}`);
    return res.json();
}

function formatCurrency(n) {
    return `$${Number(n).toFixed(2)}`;
}

function formatShortDate(isoDate) {
    const [, month, day] = isoDate.split('-');
    return `${month}/${day}`;
}

async function loadDashboard() {
    const page = document.getElementById('dashboard-page');
    const summaryUrl = page.dataset.summaryUrl;
    const transactionsUrl = page.dataset.transactionsUrl;
    const categoriesUrl = page.dataset.categoriesUrl;

    const [summaryRes, txRes, catRes] = await Promise.all([
        fetchJSON(summaryUrl),
        fetchJSON(transactionsUrl),
        fetchJSON(categoriesUrl),
    ]);

    const summary = summaryRes.data;
    const transactions = txRes.data;

    const categoryNameById = {};
    catRes.data.forEach(c => { categoryNameById[c.id] = c.name; });

    document.getElementById('balance').textContent = formatCurrency(summary.balance);
    document.getElementById('income').textContent = formatCurrency(summary.income);
    document.getElementById('expenses').textContent = formatCurrency(summary.expenses);

    renderRecentTransactions(transactions.slice(0, 5));
    renderSpendingTrend(transactions);
    renderCategoryBreakdown(transactions, categoryNameById);
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

function renderSpendingTrend(transactions) {
    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - 30);

    const byDate = {};
    transactions
        .filter(t => t.type === 'expense' && new Date(t.date) >= cutoff)
        .forEach(t => {
            byDate[t.date] = (byDate[t.date] || 0) + t.amount;
        });

    const labels = Object.keys(byDate).sort();
    const data = labels.map(d => byDate[d]);

    new Chart(document.getElementById('spending-trend-chart'), {
        type: 'line',
        data: {
            labels: labels.map(formatShortDate),
            datasets: [{
                label: 'Daily spending',
                data,
                borderColor: '#4f7c3b',
                backgroundColor: 'rgba(79, 124, 59, 0.15)',
                tension: 0.35,
                fill: true,
                pointRadius: 2,
            }],
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                x: {
                    ticks: { color: '#9c968e', maxRotation: 0, autoSkip: true, maxTicksLimit: 8 },
                    grid: { color: '#55483f' },
                },
                y: { ticks: { color: '#9c968e' }, grid: { color: '#55483f' } },
            },
        },
    });
}

function mostRecentMonthWithExpenses(transactions) {
    const expenseDates = transactions
        .filter(t => t.type === 'expense')
        .map(t => t.date)
        .sort();

    if (expenseDates.length === 0) return null;

    const latest = expenseDates[expenseDates.length - 1];
    return latest.slice(0, 7); // "YYYY-MM"
}

function renderCategoryBreakdown(transactions, categoryNameById) {
    const monthPrefix = mostRecentMonthWithExpenses(transactions);

    const byCategoryId = {};
    if (monthPrefix) {
        transactions
            .filter(t => t.type === 'expense' && t.date.startsWith(monthPrefix))
            .forEach(t => {
                byCategoryId[t.category_id] = (byCategoryId[t.category_id] || 0) + t.amount;
            });
    }

    const labels = Object.keys(byCategoryId).map(
        id => categoryNameById[id] || `Category ${id}`
    );
    const data = Object.values(byCategoryId);

    new Chart(document.getElementById('category-breakdown-chart'), {
        type: 'doughnut',
        data: {
            labels,
            datasets: [{
                data,
                backgroundColor: ['#5972b1', '#d0a650', '#962324', '#4f7c3b', '#c26f40', '#9c968e'],
                borderColor: '#201b17',
            }],
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'right', labels: { color: '#d2c8c9' } },
            },
        },
    });
}

document.addEventListener('DOMContentLoaded', () => {
    loadDashboard().catch(err => console.error('Failed to load dashboard:', err));
});
