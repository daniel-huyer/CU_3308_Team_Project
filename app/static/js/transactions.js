document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("transaction-form");
  const message = document.getElementById("transaction-message");

  if (!form || !message) {
    return;
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    message.textContent = "Transaction form is ready for backend integration.";
  });
});
