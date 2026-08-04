document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById(
        "budget-form"
    );

    const budgetIdInput = document.getElementById(
        "budget_id"
    );

    const categoryInput = document.getElementById(
        "category_id"
    );

    const monthInput = document.getElementById(
        "month"
    );

    const limitInput = document.getElementById(
        "limit_amount"
    );

    const submitButton = document.getElementById(
        "budget-submit"
    );

    const cancelEditButton = document.getElementById(
        "cancel-budget-edit"
    );

    const tableBody = document.getElementById(
        "budget-table-body"
    );

    const noBudgetsMessage = document.getElementById(
        "no-budgets-message"
    );

    const message = document.getElementById(
        "budget-message"
    );

    const listMessage = document.getElementById(
        "budget-list-message"
    );

    const formTitle = document.getElementById(
        "budget-form-title"
    );

    if (!form || !tableBody) {
        return;
    }


    function showMessage(text, isError = false) {
        if (!message) {
            return;
        }

        message.textContent = text;

        message.classList.toggle(
            "error-message",
            isError
        );

        message.classList.toggle(
            "success-message",
            !isError && text !== ""
        );
    }


    function clearMessage() {
        showMessage("");
    }


    function formatAmount(amount) {
        const numericAmount = Number(amount);

        if (!Number.isFinite(numericAmount)) {
            return "$0.00";
        }

        return numericAmount.toLocaleString(
            "en-US",
            {
                style: "currency",
                currency: "USD"
            }
        );
    }


    function getCategoryName(budget) {
        return (
            budget.category_name ||
            budget.category?.name ||
            budget.category ||
            budget.category_id ||
            "Uncategorized"
        );
    }


    function createCell(text) {
        const cell = document.createElement(
            "td"
        );

        cell.textContent = text ?? "";

        return cell;
    }


    function setDefaultMonth() {
        if (monthInput.value) {
            return;
        }

        const currentDate = new Date();

        const year =
            currentDate.getFullYear();

        const month = String(
            currentDate.getMonth() + 1
        ).padStart(2, "0");

        monthInput.value =
            `${year}-${month}`;
    }


    function buildBudgetPayload() {
        return {
            category_id: Number(
                categoryInput.value
            ),

            month: monthInput.value,

            limit_amount: Number(
                limitInput.value
            )
        };
    }


    function resetBudgetForm() {
        form.reset();

        budgetIdInput.value = "";

        categoryInput.disabled = false;
        monthInput.disabled = false;

        setDefaultMonth();

        if (formTitle) {
            formTitle.textContent =
                "Add Budget";
        }

        submitButton.textContent =
            "Add Budget";

        cancelEditButton.hidden = true;
    }


    function beginEditBudget(budget) {
        budgetIdInput.value =
            budget.id ?? "";

        categoryInput.value =
            String(
                budget.category_id ?? ""
            );

        monthInput.value =
            budget.month ?? "";

        limitInput.value =
            budget.limit_amount ?? "";

        categoryInput.disabled = true;
        monthInput.disabled = true;

        if (formTitle) {
            formTitle.textContent =
                "Edit Budget";
        }

        submitButton.textContent =
            "Update Budget";

        cancelEditButton.hidden = false;

        showMessage(
            `Editing budget ${budget.id}.`
        );

        form.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }


    function extractBudgets(result) {
        if (Array.isArray(result.data)) {
            return result.data;
        }

        if (
            Array.isArray(
                result.data?.budgets
            )
        ) {
            return result.data.budgets;
        }

        if (
            Array.isArray(
                result.budgets
            )
        ) {
            return result.budgets;
        }

        return [];
    }


    function renderBudgets(budgets) {
        tableBody.innerHTML = "";

        if (
            !Array.isArray(budgets) ||
            budgets.length === 0
        ) {
            if (noBudgetsMessage) {
                noBudgetsMessage.hidden =
                    false;

                noBudgetsMessage.textContent =
                    "No budgets found.";
            }

            return;
        }

        if (noBudgetsMessage) {
            noBudgetsMessage.hidden = true;
        }

        budgets.forEach(
            function (budget) {
                const row =
                    document.createElement(
                        "tr"
                    );

                const remainingAmount =
                    budget.remaining_amount ??
                    (
                        Number(
                            budget.limit_amount
                        ) -
                        Number(
                            budget.spent_amount ?? 0
                        )
                    );

                row.appendChild(
                    createCell(
                        budget.month
                    )
                );

                row.appendChild(
                    createCell(
                        getCategoryName(
                            budget
                        )
                    )
                );

                row.appendChild(
                    createCell(
                        formatAmount(
                            budget.limit_amount
                        )
                    )
                );

                row.appendChild(
                    createCell(
                        formatAmount(
                            budget.spent_amount ?? 0
                        )
                    )
                );

                const remainingCell =
                    createCell(
                        formatAmount(
                            remainingAmount
                        )
                    );

                if (
                    Number(
                        remainingAmount
                    ) < 0
                ) {
                    remainingCell.classList.add(
                        "error-message"
                    );
                }

                row.appendChild(
                    remainingCell
                );

                const actionsCell =
                    document.createElement(
                        "td"
                    );

                const editButton =
                    document.createElement(
                        "button"
                    );

                editButton.type =
                    "button";

                editButton.textContent =
                    "Edit";

                editButton.className =
                    "edit-budget-button";

                editButton.dataset.id =
                    budget.id;

                actionsCell.appendChild(
                    editButton
                );

                row.appendChild(
                    actionsCell
                );

                tableBody.appendChild(
                    row
                );

                editButton.addEventListener(
                    "click",
                    function () {
                        beginEditBudget(
                            budget
                        );
                    }
                );
            }
        );
    }


    async function loadCategories() {
        try {
            const response = await fetch(
                `${API_BASE}/api/categories`,
                {
                    method: "GET",

                    headers: {
                        Accept:
                            "application/json"
                    },

                    credentials: "include"
                }
            );

            const result =
                await response.json();

            if (
                !response.ok ||
                result.status !== "success"
            ) {
                throw new Error(
                    result.message ||
                    "Unable to load categories."
                );
            }

            categoryInput.innerHTML =
                '<option value="">Select Category</option>';

            result.data.forEach(
                function (category) {
                    const option =
                        document.createElement(
                            "option"
                        );

                    option.value =
                        category.id;

                    option.textContent =
                        `${category.name} (${category.type})`;

                    categoryInput.appendChild(
                        option
                    );
                }
            );

        } catch (error) {
            console.error(
                "Unable to load categories:",
                error
            );

            categoryInput.innerHTML =
                '<option value="">Unable to load categories</option>';

            categoryInput.disabled = true;

            showMessage(
                error.message ||
                "Unable to load categories.",
                true
            );
        }
    }


    async function loadBudgets() {
        tableBody.innerHTML = `
            <tr>
                <td colspan="6">
                    Loading budgets...
                </td>
            </tr>
        `;

        if (listMessage) {
            listMessage.textContent = "";
        }

        try {
            const response = await fetch(
                `${API_BASE}/api/budgets`,
                {
                    method: "GET",

                    headers: {
                        Accept:
                            "application/json"
                    },

                    credentials: "include"
                }
            );

            const result =
                await response.json();

            if (
                !response.ok ||
                result.status !== "success"
            ) {
                throw new Error(
                    result.message ||
                    "Unable to load budgets."
                );
            }

            const budgets =
                extractBudgets(result);

            renderBudgets(
                budgets
            );

        } catch (error) {
            tableBody.innerHTML = "";

            if (noBudgetsMessage) {
                noBudgetsMessage.hidden =
                    false;

                noBudgetsMessage.textContent =
                    "Unable to load budgets.";
            }

            if (listMessage) {
                listMessage.textContent =
                    error.message ||
                    "Unable to load budgets.";
            }

            showMessage(
                error.message ||
                "Unable to load budgets.",
                true
            );
        }
    }


    async function submitBudget(event) {
        event.preventDefault();

        clearMessage();

        const budgetId =
            budgetIdInput.value.trim();

        const isEditing =
            budgetId !== "";

        if (!categoryInput.value) {
            showMessage(
                "Please select a category.",
                true
            );

            return;
        }

        if (!monthInput.value) {
            showMessage(
                "Please select a month.",
                true
            );

            return;
        }

        if (limitInput.value === "") {
            showMessage(
                "Please enter a budget limit.",
                true
            );

            return;
        }

        const endpoint = isEditing
            ? `${API_BASE}/api/budgets/${budgetId}`
            : `${API_BASE}/api/budgets`;

        const method = isEditing
            ? "PUT"
            : "POST";

        const payload =
            buildBudgetPayload();

        try {
            submitButton.disabled = true;

            showMessage(
                isEditing
                    ? "Updating budget..."
                    : "Adding budget..."
            );

            const response = await fetch(
                endpoint,
                {
                    method: method,

                    headers: {
                        "Content-Type":
                            "application/json",

                        Accept:
                            "application/json"
                    },

                    credentials: "include",

                    body: JSON.stringify(
                        payload
                    )
                }
            );

            const result =
                await response.json();

            if (
                !response.ok ||
                result.status !== "success"
            ) {
                throw new Error(
                    result.message ||
                    (
                        isEditing
                            ? "Unable to update budget."
                            : "Unable to add budget."
                    )
                );
            }

            showMessage(
                result.message ||
                (
                    isEditing
                        ? "Budget updated successfully."
                        : "Budget added successfully."
                )
            );

            resetBudgetForm();

            await loadBudgets();

        } catch (error) {
            showMessage(
                error.message ||
                "Unable to save the budget.",
                true
            );

        } finally {
            submitButton.disabled = false;
        }
    }


    form.addEventListener(
        "submit",
        submitBudget
    );


    cancelEditButton?.addEventListener(
        "click",
        function () {
            resetBudgetForm();
            clearMessage();
        }
    );


    setDefaultMonth();
    loadCategories();
    loadBudgets();
});