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

  loading.style.display = "block";
  document.getElementById("result").innerText = "";
  document.getElementById("explanation").innerText = "";

  fetch("/predict", {
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .then((data) => {
      loading.style.display = "none";
      document.getElementById("result").innerText = "Result: " + data.result;
      document.getElementById("explanation").innerText = "Explanation: " + data.explanation;
    });
});
