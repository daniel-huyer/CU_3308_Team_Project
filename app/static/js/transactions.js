document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("transaction-form");
  const transactionIdInput = document.getElementById("transaction_id");
  const typeInput = document.getElementById("type");
  const amountInput = document.getElementById("amount");
  const categoryInput = document.getElementById("category_id");
  const dateInput = document.getElementById("date");
  const noteInput = document.getElementById("note");

  const submitButton = document.getElementById(
    "submit-transaction-button"
  );
  const cancelEditButton = document.getElementById(
    "cancel-edit-button"
  );

  const message = document.getElementById("transaction-message");

  const searchInput = document.getElementById("transaction-search");
  const typeFilter = document.getElementById(
    "transaction-type-filter"
  );
  const applyFiltersButton = document.getElementById(
    "apply-transaction-filters"
  );
  const clearFiltersButton = document.getElementById(
    "clear-transaction-filters"
  );

  const tableBody = document.getElementById(
    "transactions-table-body"
  );
  const noTransactionsMessage = document.getElementById(
    "no-transactions-message"
  );

  if (!form || !tableBody) {
    return;
  }

  function showMessage(text, isError = false) {
    if (!message) {
      return;
    }

    message.textContent = text;

    message.classList.toggle("error-message", isError);
    message.classList.toggle(
      "success-message",
      !isError && text !== ""
    );
  }

  function clearMessage() {
    showMessage("");
  }

  function buildQueryString() {
    const parameters = new URLSearchParams();

    const searchValue = searchInput?.value.trim();
    const typeValue = typeFilter?.value;

    if (searchValue) {
      parameters.set("search", searchValue);
    }

    if (typeValue) {
      parameters.set("type", typeValue);
    }

    const queryString = parameters.toString();

    return queryString ? `?${queryString}` : "";
  }

  function formatAmount(amount) {
    const numericAmount = Number(amount);

    if (!Number.isFinite(numericAmount)) {
      return "";
    }

    return numericAmount.toLocaleString("en-US", {
      style: "currency",
      currency: "USD"
    });
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

  function createCell(text) {
    const cell = document.createElement("td");
    cell.textContent = text ?? "";
    return cell;
  }

  function renderTransactions(transactions) {
    tableBody.innerHTML = "";

    if (!Array.isArray(transactions) || transactions.length === 0) {
      if (noTransactionsMessage) {
        noTransactionsMessage.hidden = false;
      }

      return;
    }

    if (noTransactionsMessage) {
      noTransactionsMessage.hidden = true;
    }

    transactions.forEach(function (transaction) {
      const row = document.createElement("tr");

      row.appendChild(createCell(transaction.date));
      row.appendChild(createCell(transaction.type));
      row.appendChild(createCell(getCategoryName(transaction)));
      row.appendChild(createCell(formatAmount(transaction.amount)));
      row.appendChild(
        createCell(transaction.note || transaction.description || "")
      );

      const actionsCell = document.createElement("td");

      const editButton = document.createElement("button");
      editButton.type = "button";
      editButton.textContent = "Edit";
      editButton.className = "edit-transaction-button";
      editButton.dataset.id = transaction.id;

      const deleteButton = document.createElement("button");
      deleteButton.type = "button";
      deleteButton.textContent = "Delete";
      deleteButton.className = "delete-transaction-button";
      deleteButton.dataset.id = transaction.id;

      actionsCell.appendChild(editButton);
      actionsCell.appendChild(document.createTextNode(" "));
      actionsCell.appendChild(deleteButton);

      row.appendChild(actionsCell);
      tableBody.appendChild(row);

      editButton.addEventListener("click", function () {
        beginEditTransaction(transaction);
      });
    });
  }

  function extractTransactions(result) {
    if (Array.isArray(result.data)) {
      return result.data;
    }

    if (Array.isArray(result.data?.transactions)) {
      return result.data.transactions;
    }

    if (Array.isArray(result.transactions)) {
      return result.transactions;
    }

    return [];
  }

  async function loadTransactions() {
    const queryString = buildQueryString();

    clearMessage();

    try {
      const response = await fetch(
        `/api/transactions${queryString}`,
        {
          method: "GET",
          headers: {
            Accept: "application/json"
          }
        }
      );

      const result = await response.json();

      if (!response.ok || result.status !== "success") {
        throw new Error(
          result.message || "Unable to load transactions."
        );
      }

      const transactions = extractTransactions(result);

      renderTransactions(transactions);
    } catch (error) {
      tableBody.innerHTML = "";

      if (noTransactionsMessage) {
        noTransactionsMessage.hidden = false;
        noTransactionsMessage.textContent =
          "Unable to load transactions.";
      }

      showMessage(error.message, true);
    }
  }

  function buildTransactionPayload() {
    return {
      type: typeInput.value,
      amount: Number(amountInput.value),
      category_id: Number(categoryInput.value),
      date: dateInput.value,
      note: noteInput.value.trim()
    };
  }

  async function submitTransaction(event) {
    event.preventDefault();

    clearMessage();

    const transactionId = transactionIdInput.value;
    const isEditing = transactionId !== "";

    const endpoint = isEditing
      ? `/api/transactions/${transactionId}`
      : "/api/transactions";

    const method = isEditing ? "PUT" : "POST";
    const payload = buildTransactionPayload();

    try {
      submitButton.disabled = true;

      const response = await fetch(endpoint, {
        method: method,
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json"
        },
        body: JSON.stringify(payload)
      });

      const result = await response.json();

      if (!response.ok || result.status !== "success") {
        throw new Error(
          result.message ||
            `Unable to ${isEditing ? "update" : "add"} transaction.`
        );
      }

      showMessage(
        result.message ||
          `Transaction ${
            isEditing ? "updated" : "added"
          } successfully.`
      );

      resetTransactionForm();
      await loadTransactions();
    } catch (error) {
      showMessage(error.message, true);
    } finally {
      submitButton.disabled = false;
    }
  }

  function beginEditTransaction(transaction) {
    transactionIdInput.value = transaction.id ?? "";
    typeInput.value = transaction.type ?? "";
    amountInput.value = transaction.amount ?? "";
    categoryInput.value = transaction.category_id ?? "";
    dateInput.value = transaction.date ?? "";
    noteInput.value =
      transaction.note || transaction.description || "";

    submitButton.textContent = "Update Transaction";
    cancelEditButton.hidden = false;

    form.scrollIntoView({
      behavior: "smooth",
      block: "start"
    });
  }

  function resetTransactionForm() {
    form.reset();
    transactionIdInput.value = "";
    submitButton.textContent = "Add Transaction";
    cancelEditButton.hidden = true;
  }

  async function deleteTransaction(transactionId) {
    const confirmed = window.confirm(
      "Are you sure you want to delete this transaction?"
    );

    if (!confirmed) {
      return;
    }

    clearMessage();

    try {
      const response = await fetch(
        `/api/transactions/${transactionId}`,
        {
          method: "DELETE",
          headers: {
            Accept: "application/json"
          }
        }
      );

      const result = await response.json();

      if (!response.ok || result.status !== "success") {
        throw new Error(
          result.message || "Unable to delete transaction."
        );
      }

      showMessage(
        result.message || "Transaction deleted successfully."
      );

      await loadTransactions();
    } catch (error) {
      showMessage(error.message, true);
    }
  }

  form.addEventListener("submit", submitTransaction);

  cancelEditButton?.addEventListener("click", function () {
    resetTransactionForm();
    clearMessage();
  });

  applyFiltersButton?.addEventListener(
    "click",
    loadTransactions
  );

  clearFiltersButton?.addEventListener("click", function () {
    if (searchInput) {
      searchInput.value = "";
    }

    if (typeFilter) {
      typeFilter.value = "";
    }

    loadTransactions();
  });

  searchInput?.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      loadTransactions();
    }
  });

  tableBody.addEventListener("click", function (event) {
    const deleteButton = event.target.closest(
      ".delete-transaction-button"
    );

    if (!deleteButton) {
      return;
    }

    const transactionId = deleteButton.dataset.id;

    if (!transactionId) {
      showMessage("Transaction ID is missing.", true);
      return;
    }

    deleteTransaction(transactionId);
  });

  loadTransactions();
});