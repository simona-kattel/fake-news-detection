const dropArea = document.getElementById("dropArea");
const fileInput = document.getElementById("fileInput");
const checkBtn = document.getElementById("checkBtn");
const loading = document.getElementById("loading");

dropArea.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", () => {
  dropArea.innerText = "✅ File uploaded: " + fileInput.files[0].name;
  checkBtn.style.display = "inline-block";
});

document.getElementById("uploadForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const formData = new FormData(this);
  showLoading();
  fetch("/predict", {
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .then((data) => {
      window.location.href = `/result?result=${encodeURIComponent(data.result)}&explanation=${encodeURIComponent(data.explanation)}`;
    });
});

document.getElementById("urlForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const urlInput = document.getElementById("urlInput").value;
  showLoading();
  fetch("/predict_url", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url: urlInput }),
  })
    .then((res) => res.json())
    .then((data) => {
      window.location.href = `/result?result=${encodeURIComponent(data.result)}&explanation=${encodeURIComponent(data.explanation)}`;
    });
});

function showLoading() {
  loading.style.display = "block";
}
