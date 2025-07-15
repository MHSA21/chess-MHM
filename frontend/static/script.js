document.addEventListener("DOMContentLoaded", () => {
  const analyzeBtn = document.getElementById("analyzeBtn");
  const fenInput = document.getElementById("fenInput");
  const ratingInput = document.getElementById("ratingInput");
  const styleSelect = document.getElementById("styleSelect");
  const resultDiv = document.getElementById("result");

  analyzeBtn.addEventListener("click", async () => {
    const fen = fenInput.value.trim();
    const rating = parseInt(ratingInput.value);
    const style = styleSelect.value;

    if (!fen || isNaN(rating)) {
      resultDiv.textContent = "Please provide valid inputs.";
      return;
    }

    resultDiv.textContent = "Analyzing...";

    try {
      const response = await fetch("/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ fen, rating, style })
      });

      const data = await response.json();
      resultDiv.textContent = data.best_move
        ? `Best Move: ${data.best_move}`
        : "No move found.";
    } catch (error) {
      resultDiv.textContent = "Error: " + error.message;
    }
  });
});
