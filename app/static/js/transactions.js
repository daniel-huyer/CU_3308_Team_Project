document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById(
        "transaction-form"
    );

    const transactionIdInput = document.getElementById(
        "transaction_id"
    );

    const typeInput = document.getElementById(
        "type"
    );

    const amountInput = document.getElementById(
        "amount"
    );

    const categoryInput = document.getElementById(
        "category_id"
    );

    const dateInput = document.getElementById(
        "date"
    );

    const noteInput = document.getElementById(
        "note"
    );

    const submitButton = document.getElementById(
        "transaction-submit"
    );

    const cancelEditButton = document.getElementById(
        "cancel-edit"
    );

    const searchInput = document.getElementById(
        "search-keyword"
    );

    const typeFilter = document.getElementById(
        "filter-type"
    );

    const categoryFilter = document.getElementById(
        "filter-category"
    );

    const startDateFilter = document.getElementById(
        "filter-start-date"
    );

    const endDateFilter = document.getElementById(
        "filter-end-date"
    );

    const filterForm = document.getElementById(
        "transaction-filter-form"
    );

    const clearFiltersButton = document.getElementById(
        "clear-filters"
    );

    const tableBody = document.getElementById(
        "transaction-table-body"
    );

    const noTransactionsMessage = document.getElementById(
        "no-transactions-message"
    );

    const message = document.getElementById(
        "transaction-message"
    );

    const historyMessage = document.getElementById(
        "history-message"
    );

    const formTitle = document.getElementById(
        "transaction-form-title"
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
            return "";
        }

        return numericAmount.toLocaleString(
            "en-US",
            {
                style: "currency",
                currency: "USD"
            }
        );
    }


    function getCategoryName(transaction) {
        return (
            transaction.category_name ||
            transaction.category?.name ||
            transaction.category ||
            transaction.category_id ||
            "Uncategorized"
        );
    }


    const CATEGORY_COLORS = {
        Food: "#3b82f6",
        Transportation: "#f5b942",
        Utilities: "#ef4444",
        Entertainment: "#22c55e",
        Healthcare: "#fb923c",
        Housing: "#a855f7",
        Gift: "#06b6d4",
        Paycheck: "#10b981"
    };
    function getCategoryColor(categoryName) {
        return CATEGORY_COLORS[categoryName] || "#6b7280";
    }
    function createCell(text) {
        const cell = document.createElement(
            "td"
        );

        cell.textContent = text ?? "";

        return cell;
    }


    function buildQueryString() {
        const parameters = new URLSearchParams();

        const searchValue =
            searchInput?.value.trim();

        const typeValue =
            typeFilter?.value;

        const categoryValue =
            categoryFilter?.value;

        const startDateValue =
            startDateFilter?.value;

        const endDateValue =
            endDateFilter?.value;

        if (searchValue) {
            parameters.set(
                "keyword",
                searchValue
            );
        }

        if (typeValue) {
            parameters.set(
                "type",
                typeValue
            );
        }

        if (categoryValue) {
            parameters.set(
                "category_id",
                categoryValue
            );
        }

        if (startDateValue) {
            parameters.set(
                "start_date",
                startDateValue
            );
        }

        if (endDateValue) {
            parameters.set(
                "end_date",
                endDateValue
            );
        }

        const queryString =
            parameters.toString();

        return queryString
            ? `?${queryString}`
            : "";
    }


    function buildTransactionPayload() {
        return {
            type: typeInput.value,

            amount: Number(
                amountInput.value
            ),

            category_id: Number(
                categoryInput.value
            ),

            date: dateInput.value,

            note: noteInput.value.trim()
        };
    }


    function setDefaultDate() {
        if (!dateInput.value) {
            dateInput.value =
                new Date()
                    .toISOString()
                    .split("T")[0];
        }
    }


    function resetTransactionForm() {
        form.reset();

        transactionIdInput.value = "";

        setDefaultDate();

        if (formTitle) {
            formTitle.textContent =
                "Add Transaction";
        }

        submitButton.textContent =
            "Add Transaction";

        cancelEditButton.hidden = true;
    }


    function beginEditTransaction(transaction) {
        transactionIdInput.value =
            transaction.id ?? "";

        typeInput.value =
            transaction.type ?? "";

        amountInput.value =
            transaction.amount ?? "";

        categoryInput.value =
            transaction.category_id ?? "";

        dateInput.value =
            transaction.date ?? "";

        noteInput.value =
            transaction.note ||
            transaction.description ||
            "";

        if (formTitle) {
            formTitle.textContent =
                "Edit Transaction";
        }

        submitButton.textContent =
            "Update Transaction";

        cancelEditButton.hidden = false;

        if (historyMessage) {
            historyMessage.textContent =
                `Editing transaction ${transaction.id}.`;
        }

        form.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }


    function extractTransactions(result) {
        if (Array.isArray(result.data)) {
            return result.data;
        }

        if (
            Array.isArray(
                result.data?.transactions
            )
        ) {
            return result.data.transactions;
        }

        if (
            Array.isArray(
                result.transactions
            )
        ) {
            return result.transactions;
        }

        return [];
    }


    function renderTransactions(transactions) {
        tableBody.innerHTML = "";

        if (
            !Array.isArray(transactions) ||
            transactions.length === 0
        ) {
            if (noTransactionsMessage) {
                noTransactionsMessage.hidden =
                    false;

                noTransactionsMessage.textContent =
                    "No transactions found.";
            }

            return;
        }

        if (noTransactionsMessage) {
            noTransactionsMessage.hidden = true;
        }

        transactions.forEach(
            function (transaction) {
                const row =
                    document.createElement(
                        "tr"
                    );

                row.appendChild(
                    createCell(
                        transaction.date
                    )
                );

                row.appendChild(
                    createCell(
                        transaction.note ||
                        transaction.description ||
                        ""
                    )
                );

                const categoryCell = document.createElement("td");
                const categoryName = getCategoryName(transaction);
                const categoryBadge = document.createElement("span");
                categoryBadge.textContent = categoryName;
                categoryBadge.style.color = getCategoryColor(categoryName);
                categoryBadge.style.fontWeight = "600";
                categoryCell.appendChild(categoryBadge);
                row.appendChild(categoryCell);

                row.appendChild(
                    createCell(
                        transaction.type
                    )
                );

                row.appendChild(
                    createCell(
                        formatAmount(
                            transaction.amount
                        )
                    )
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
                    "btn btn-secondary edit-transaction-button";

                editButton.dataset.id =
                    transaction.id;

                const deleteButton =
                    document.createElement(
                        "button"
                    );

                deleteButton.type =
                    "button";

                deleteButton.textContent =
                    "Delete";

                deleteButton.className =
                    "btn btn-danger delete-transaction-button";

                deleteButton.dataset.id =
                    transaction.id;

                actionsCell.appendChild(
                    editButton
                );

                actionsCell.appendChild(
                    document.createTextNode(
                        " "
                    )
                );

                actionsCell.appendChild(
                    deleteButton
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
                        beginEditTransaction(
                            transaction
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

            categoryFilter.innerHTML =
                '<option value="">All Categories</option>';

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

                    categoryFilter.appendChild(
                        option.cloneNode(true)
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


    async function loadTransactions() {
        const queryString =
            buildQueryString();

        if (historyMessage) {
            historyMessage.textContent = "";
        }

        tableBody.innerHTML = `
            <tr>
                <td colspan="6">
                    Loading transactions...
                </td>
            </tr>
        `;

        try {
            const response = await fetch(
                `${API_BASE}/api/transactions${queryString}`,
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
                    "Unable to load transactions."
                );
            }

            const transactions =
                extractTransactions(result);

            renderTransactions(
                transactions
            );

        } catch (error) {
            tableBody.innerHTML = "";

            if (noTransactionsMessage) {
                noTransactionsMessage.hidden =
                    false;

                noTransactionsMessage.textContent =
                    "Unable to load transactions.";
            }

            if (historyMessage) {
                historyMessage.textContent =
                    error.message ||
                    "Unable to load transactions.";
            }

            showMessage(
                error.message ||
                "Unable to load transactions.",
                true
            );
        }
    }


    async function submitTransaction(event) {
        event.preventDefault();

        clearMessage();

        const transactionId =
            transactionIdInput.value.trim();

        const isEditing =
            transactionId !== "";

        if (!typeInput.value) {
            showMessage(
                "Please select a transaction type.",
                true
            );

            return;
        }

        if (amountInput.value === "") {
            showMessage(
                "Please enter an amount.",
                true
            );

            return;
        }

        if (!categoryInput.value) {
            showMessage(
                "Please select a category.",
                true
            );

            return;
        }

        if (!dateInput.value) {
            showMessage(
                "Please select a date.",
                true
            );

            return;
        }

        const endpoint = isEditing
            ? `${API_BASE}/api/transactions/${transactionId}`
            : `${API_BASE}/api/transactions`;

        const method = isEditing
            ? "PUT"
            : "POST";

        const payload =
            buildTransactionPayload();

        try {
            submitButton.disabled = true;

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
                            ? "Unable to update transaction."
                            : "Unable to add transaction."
                    )
                );
            }

            showMessage(
                result.message ||
                (
                    isEditing
                        ? "Transaction updated successfully."
                        : "Transaction added successfully."
                )
            );

            resetTransactionForm();

            await loadTransactions();

        } catch (error) {
            showMessage(
                error.message ||
                "Unable to save the transaction.",
                true
            );

        } finally {
            submitButton.disabled = false;
        }
    }


    async function deleteTransaction(
        transactionId
    ) {
        const confirmed = window.confirm(
            "Are you sure you want to delete this transaction?"
        );

        if (!confirmed) {
            return;
        }

        clearMessage();

        try {
            const response = await fetch(
                `${API_BASE}/api/transactions/${transactionId}`,
                {
                    method: "DELETE",

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
                    "Unable to delete transaction."
                );
            }

            showMessage(
                result.message ||
                "Transaction deleted successfully."
            );

            await loadTransactions();

        } catch (error) {
            showMessage(
                error.message ||
                "Unable to delete transaction.",
                true
            );
        }
    }


    form.addEventListener(
        "submit",
        submitTransaction
    );


    cancelEditButton?.addEventListener(
        "click",
        function () {
            resetTransactionForm();
            clearMessage();
        }
    );


    filterForm?.addEventListener(
        "submit",
        function (event) {
            event.preventDefault();

            loadTransactions();
        }
    );


    clearFiltersButton?.addEventListener(
        "click",
        function () {
            if (searchInput) {
                searchInput.value = "";
            }

            if (typeFilter) {
                typeFilter.value = "";
            }

            if (categoryFilter) {
                categoryFilter.value = "";
            }

            if (startDateFilter) {
                startDateFilter.value = "";
            }

            if (endDateFilter) {
                endDateFilter.value = "";
            }

            loadTransactions();
        }
    );


    searchInput?.addEventListener(
        "keydown",
        function (event) {
            if (event.key === "Enter") {
                event.preventDefault();

                loadTransactions();
            }
        }
    );


    tableBody.addEventListener(
        "click",
        function (event) {
            const deleteButton =
                event.target.closest(
                    ".delete-transaction-button"
                );

            if (!deleteButton) {
                return;
            }

            const transactionId =
                deleteButton.dataset.id;

            if (!transactionId) {
                showMessage(
                    "Transaction ID is missing.",
                    true
                );

                return;
            }

            deleteTransaction(
                transactionId
            );
        }
    );


    setDefaultDate();
    loadCategories();
    loadTransactions();
});