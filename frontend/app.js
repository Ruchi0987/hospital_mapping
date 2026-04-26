const form = document.getElementById("searchForm");
const input = document.getElementById("diseaseInput");
const results = document.getElementById("results");
const modelInfo = document.getElementById("modelInfo");

const API_BASE = "http://localhost:8000";

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  results.innerHTML = "";
  modelInfo.textContent = "Searching...";

  const disease = input.value.trim();
  const response = await fetch(`${API_BASE}/api/suggest`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ disease }),
  });

  if (!response.ok) {
    modelInfo.textContent = "Something went wrong. Try again.";
    return;
  }

  const data = await response.json();
  modelInfo.textContent = `Model: ${data.model}`;

  if (!data.suggestions.length) {
    results.innerHTML = "<p>No strong match found. Try a more specific disease.</p>";
    return;
  }

  data.suggestions.forEach((hospital) => {
    const card = document.createElement("article");
    card.className = "card";
    card.innerHTML = `
      <h3>${hospital.name}</h3>
      <p><strong>Departments:</strong> ${hospital.departments.join(", ")}</p>
      <p><strong>Location:</strong> ${hospital.location}</p>
      <p><strong>Contact:</strong> ${hospital.contact}</p>
      <p><strong>AI Match Score:</strong> ${hospital.match_score}</p>
    `;
    results.appendChild(card);
  });
});
