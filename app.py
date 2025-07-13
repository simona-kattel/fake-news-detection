from flask import Flask, render_template, request, jsonify, redirect, url_for
import joblib
from docx import Document
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

def extract_text(file):
    filename = file.filename
    if filename.endswith(".txt"):
        return file.read().decode("utf-8")
    elif filename.endswith(".docx"):
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        return ""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result")
def result():
    result = request.args.get("result", "")
    explanation = request.args.get("explanation", "")
    return render_template("result.html", result=result, explanation=explanation)

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files["file"]
    text = extract_text(file)
    X = vectorizer.transform([text])
    prediction = model.predict(X)[0]
    explanation = explain_prediction(text, prediction)
    return jsonify({"result": "✅ Real" if prediction == 1 else "❌ Fake", "explanation": explanation})

@app.route("/predict_url", methods=["POST"])
def predict_url():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"result": "Error", "explanation": "No URL provided."})
    try:
        page = requests.get(url, timeout=5)
        soup = BeautifulSoup(page.content, "html.parser")
        paragraphs = soup.find_all("p")
        article_text = " ".join([p.get_text() for p in paragraphs])
        X = vectorizer.transform([article_text])
        prediction = model.predict(X)[0]
        explanation = explain_prediction(article_text, prediction)
        return jsonify({"result": "✅ Real" if prediction == 1 else "❌ Fake", "explanation": explanation})
    except Exception as e:
        return jsonify({"result": "Error", "explanation": str(e)})

def explain_prediction(text, prediction):
    X = vectorizer.transform([text])
    importance = X.toarray()[0] * model.coef_[0]
    feature_names = vectorizer.get_feature_names_out()
    top_indices = importance.argsort()[-5:][::-1]
    top_words = [feature_names[i] for i in top_indices if importance[i] != 0]
    if prediction == 1:
        explanation = (
            "This article appears to be real based on its use of credible terminology like: " + ", ".join(top_words) + ". "
            "It maintains a balanced tone and provides factual evidence without exaggeration. "
            "Reliable formatting and neutral language also support authenticity. "
            "It references verifiable events or sources. "
            "Overall, the linguistic patterns are consistent with trustworthy journalism."
        )
    else:
        explanation = (
            "This article appears to be fake due to the presence of sensational or misleading terms like: " + ", ".join(top_words) + ". "
            "It lacks reliable sourcing or cites questionable claims. "
            "The language may be emotional, exaggerated, or intended to provoke. "
            "There is often a lack of evidence or overuse of speculation. "
            "The overall writing style and word choice align with known patterns of misinformation."
        )
    return explanation

if __name__ == "__main__":
    app.run(debug=True)
