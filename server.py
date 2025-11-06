from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# 🔹 Folder where uploaded files are stored
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🟢 Upload a file to a subject folder
@app.route("/upload", methods=["POST"])
def upload_file():
    subject = request.form.get("subject")
    file = request.files.get("file")

    if not subject or not file:
        return jsonify({"error": "No subject or file"}), 400

    subject_folder = os.path.join(app.config["UPLOAD_FOLDER"], subject)
    os.makedirs(subject_folder, exist_ok=True)

    filepath = os.path.join(subject_folder, secure_filename(file.filename))
    file.save(filepath)

    return jsonify({
        "message": "✅ File uploaded successfully!",
        "filename": file.filename
    })

# 📂 List all files under a subject
@app.route("/files/<subject>")
def list_files(subject):
    subject_folder = os.path.join(app.config["UPLOAD_FOLDER"], subject)
    if not os.path.exists(subject_folder):
        return jsonify([])
    return jsonify(os.listdir(subject_folder))

# 📄 Serve a specific uploaded file
@app.route("/uploads/<subject>/<filename>")
def serve_file(subject, filename):
    subject_folder = os.path.join(app.config["UPLOAD_FOLDER"], subject)
    return send_from_directory(subject_folder, filename)

# ❌ Delete a file from a subject folder
@app.route("/delete/<subject>/<filename>", methods=["DELETE"])
def delete_file(subject, filename):
    subject_folder = os.path.join(app.config["UPLOAD_FOLDER"], subject)
    filepath = os.path.join(subject_folder, filename)

    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({"message": "🗑️ File deleted successfully"})
    return jsonify({"error": "File not found"}), 404

# 📘 List all available subjects (folders)
@app.route("/subjects")
def list_subjects():
    folders = [
        d for d in os.listdir(UPLOAD_FOLDER)
        if os.path.isdir(os.path.join(UPLOAD_FOLDER, d))
    ]
    return jsonify(folders)

# 🟣 Home route for Render health check
@app.route("/")
def home():
    return jsonify({"message": "📚 Flask File Server is running!"})

# 🚀 Main entry (Render uses PORT environment variable)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
