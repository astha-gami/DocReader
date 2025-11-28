from flask import Flask, request, jsonify, render_template
import os
from ai_engine.engine import analyze_document

app = Flask(__name__)

# Folder to store uploaded PDFs temporarily
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ----------------------
# FRONTEND HOME PAGE
# ----------------------
@app.route("/")
def index():
    return render_template("index.html")


# ----------------------
# PDF ANALYZE API
# ----------------------
@app.route("/analyze", methods=["POST"])
def analyze_file():

    # Check if file is included in request
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Save uploaded PDF
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    try:
        # Run your AI engine
        result = analyze_document(file_path)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------------------
# RUN SERVER
# ----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

