from flask import Flask, render_template, request, jsonify
import joblib
from docx import Document

app = Flask(__name__)

# Load model and vectorizer
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

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files["file"]
    text = extract_text(file)

    # Transform and predict
    X = vectorizer.transform([text])
    prediction = model.predict(X)[0]

    # Generate explanation (top influencing words)
    importance = X.toarray()[0] * model.coef_[0]
    feature_names = vectorizer.get_feature_names_out()
    top_indices = importance.argsort()[-5:][::-1]
    top_words = [feature_names[i] for i in top_indices]
    explanation = "Top contributing words: " + ", ".join(top_words)

    return jsonify({
        "result": "✅ Real" if prediction == 1 else "❌ Fake",
        "explanation": explanation
    })

if __name__ == "__main__":
    print("Running Flask server...")
    app.run(debug=True)

