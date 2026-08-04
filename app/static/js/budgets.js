// app/static/js/budgets.js

async function fetchJSON(url, options) {
    const res = await fetch(url, options);
    const body = await res.json().catch(() => ({}));
    if (!res.ok) {
        const err = new Error(body.message || `Request to ${url} failed: ${res.status}`);
        err.status = res.status;
        err.body = body;
        throw err;
    }
    return body;
}

function formatCurrency(n) {
    return `$${Number(n).toFixed(2)}`;
}

function currentMonth() {
    const now = new Date();
    return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
}

let categoriesById = {};
let expenseCategories = [];
let page;

async function init() {
    page = document.getElementById('budgets-page');

    const monthInput = document.getElementById('budget-month');
    monthInput.value = currentMonth();
    document.getElementById('budget-list-month').textContent = currentMonth();

    const catRes = await fetchJSON(page.dataset.categoriesUrl);
    categoriesById = {};
    catRes.data.forEach(c => { categoriesById[c.id] = c; });
    expenseCategories = catRes.data.filter(c => c.type === 'expense');

    populateCategoryDropdown();
    await refreshBudgetList();

    document.getElementById('budget-form').addEventListener('submit', handleSubmit);
    monthInput.addEventListener('change', () => {
        document.getElementById('budget-list-month').textContent = monthInput.value;
        refreshBudgetList();
    });
}

function populateCategoryDropdown() {
    const select = document.getElementById('budget-category');
    select.innerHTML = '<option value="">Select Category</option>';
    expenseCategories.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c.id;
        opt.textContent = c.name;
        select.appendChild(opt);
    });
}

async function handleSubmit(e) {
    e.preventDefault();
    const messageEl = document.getElementById('budget-form-message');
    messageEl.textContent = '';
    messageEl.className = '';

    const month = document.getElementById('budget-month').value;
    const categoryId = document.getElementById('budget-category').value;
    const limitAmount = document.getElementById('budget-limit').value;

    try {
        await fetchJSON(page.dataset.budgetsUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                month,
                category_id: Number(categoryId),
                limit_amount: Number(limitAmount),
            }),
        });
        messageEl.textContent = 'Budget saved.';
        messageEl.className = 'inline-success';
        document.getElementById('budget-form').reset();
        document.getElementById('budget-month').value = month;
        await refreshBudgetList();
    } catch (err) {
        if (err.status === 409) {
            messageEl.textContent = 'A budget already exists for this category and month. Edit it in the list below instead.';
        } else {
            messageEl.textContent = err.message || 'Failed to save budget.';
        }
        messageEl.className = 'inline-error';
    }
}

async function refreshBudgetList() {
    const month = document.getElementById('budget-month').value;
    const [budgetsRes, txRes] = await Promise.all([
        fetchJSON(page.dataset.budgetsUrl),
        fetchJSON(page.dataset.transactionsUrl),
    ]);

    const budgetsForMonth = budgetsRes.data.filter(b => b.month === month);
    const spentByCategory = {};
    txRes.data
        .filter(t => t.type === 'expense' && t.date.startsWith(month))
        .forEach(t => {
            spentByCategory[t.category_id] = (spentByCategory[t.category_id] || 0) + t.amount;
        });

    renderBudgetList(budgetsForMonth, spentByCategory);
}

function renderBudgetList(budgets, spentByCategory) {
    const container = document.getElementById('budget-list');
    container.innerHTML = '';

    if (budgets.length === 0) {
        container.innerHTML = '<p class="muted">No budgets set for this month yet.</p>';
        return;
    }

    budgets.forEach(b => {
        const spent = spentByCategory[b.category_id] || 0;
        const pct = Math.min(100, (spent / b.limit_amount) * 100);
        const over = spent > b.limit_amount;
        const category = categoriesById[b.category_id];
        const categoryName = category ? category.name : `Category ${b.category_id}`;

        const row = document.createElement('div');
        row.className = 'card';
        row.style.marginBottom = '0.75rem';

        row.innerHTML = `
            <div style="display:flex; justify-content:space-between;">
                <strong>${categoryName}</strong>
                <span class="${over ? 'amount-expense' : ''}">${formatCurrency(spent)} / ${formatCurrency(b.limit_amount)}</span>
            </div>
            <div class="progress-bar">
                <div class="progress-bar-fill ${over ? 'over-budget' : ''}" style="width:${pct}%"></div>
            </div>
            ${over ? '<p class="inline-error">Over budget</p>' : ''}
            <div class="row-actions" style="margin-top:0.5rem;">
                <input type="number" step="0.01" min="0.01" class="edit-limit-input" data-budget-id="${b.id}" value="${b.limit_amount}" style="width:100px;">
                <button type="button" class="btn save-limit-btn" data-budget-id="${b.id}">Update Limit</button>
            </div>
        `;

        container.appendChild(row);
    });

    container.querySelectorAll('.save-limit-btn').forEach(btn => {
        btn.addEventListener('click', () => handleUpdateLimit(btn.dataset.budgetId));
    });
}

async function handleUpdateLimit(budgetId) {
    const input = document.querySelector(`.edit-limit-input[data-budget-id="${budgetId}"]`);
    const newLimit = Number(input.value);

    try {
        await fetchJSON(`${page.dataset.budgetsUrl}/${budgetId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ limit_amount: newLimit }),
        });
        await refreshBudgetList();
    } catch (err) {
        alert(err.message || 'Failed to update budget.');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    init().catch(err => console.error('Failed to load budgets page:', err));
});
