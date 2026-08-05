// app/static/js/dashboard.js

const CATEGORY_COLORS = {
    Food: '#3b82f6',
    Transportation: '#f5b942',
    Utilities: '#ef4444',
    Entertainment: '#22c55e',
    Healthcare: '#fb923c',
    Housing: '#a855f7',
    Gift: '#06b6d4',
    Paycheck: '#10b981',
};
function getCategoryColor(categoryName) {
    return CATEGORY_COLORS[categoryName] || '#6b7280';
}

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

    renderRecentTransactions(transactions.slice(0, 5), categoryNameById);
    renderSpendingTrend(transactions);
    renderCategoryBreakdown(transactions, categoryNameById);
}

function renderRecentTransactions(transactions, categoryNameById) {
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

        const categoryName = categoryNameById[t.category_id] || 'Uncategorized';

        const label = document.createElement('span');
        const categoryTag = document.createElement('span');
        categoryTag.textContent = categoryName;
        categoryTag.style.color = getCategoryColor(categoryName);
        categoryTag.style.fontWeight = '600';
        categoryTag.style.display = 'inline-block';
        categoryTag.style.minWidth = '140px';
        categoryTag.style.marginRight = '0.5rem';
        label.appendChild(categoryTag);
        label.appendChild(document.createTextNode(t.description || '(no description)'));

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
                borderColor: '#1a1a1a',
                backgroundColor: 'rgba(26, 26, 26, 0.08)',
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
                    ticks: { color: '#6b7280', maxRotation: 0, autoSkip: true, maxTicksLimit: 8 },
                    grid: { color: '#e2e5ea' },
                },
                y: { ticks: { color: '#6b7280' }, grid: { color: '#e2e5ea' } },
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
    const colors = labels.map(getCategoryColor);

    new Chart(document.getElementById('category-breakdown-chart'), {
        type: 'doughnut',
        data: {
            labels,
            datasets: [{
                data,
                backgroundColor: colors,
                borderColor: '#ffffff',
            }],
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'right', labels: { color: '#1a1a1a' } },
            },
        },
    });
}

document.addEventListener('DOMContentLoaded', () => {
    loadDashboard().catch(err => console.error('Failed to load dashboard:', err));
});
