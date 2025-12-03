# === ADD THESE IMPORTS ===
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import bcrypt
from datetime import datetime
import os
from dotenv import load_dotenv
# =========================

app = Flask(__name__)
app.config['SECRET_KEY'] = 'docreader-astha-2707'  # Change this!

# Enable CORS (for frontend communication)
CORS(app)

# === ADD THESE LINES FOR MONGODB ===
# Load environment variables (we'll create .env file)
load_dotenv()

# Get MongoDB connection string from environment or use directly
MONGO_URI = os.getenv('MONGO_URI') or "mongodb+srv://asthagami2707_db_user:ZiNSWzq6cW79XDuD@cluster0.hypc9k3.mongodb.net/?appName=Cluster0"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["docreader_db"]  # Database name
users_collection = db["users"]  # Collection for user accounts
documents_collection = db["documents"]  # Collection for uploaded documents

print("✅ Connected to MongoDB!")
# ====================================
# ===== USER REGISTRATION ENDPOINT =====
@app.route('/api/register', methods=['POST'])
def register():
    try:
        # Get data from request
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        # Validate input
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        # Check if user already exists
        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            return jsonify({"error": "Email already registered"}), 400
        
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create user document
        user = {
            "email": email,
            "password": hashed_password.decode('utf-8'),  # Store as string
            "created_at": datetime.utcnow(),
            "daily_uploads": 0,
            "last_reset": datetime.utcnow(),
            "plan": "free"  # free users get 10 uploads/day
        }
        
        # Insert into database
        result = users_collection.insert_one(user)
        
        return jsonify({
            "message": "Registration successful!",
            "user_id": str(result.inserted_id),
            "email": email
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

 # ===== USER LOGIN ENDPOINT =====
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        # Find user by email
        user = users_collection.find_one({"email": email})
        
        if not user:
            return jsonify({"error": "Invalid email or password"}), 401
        
        # Check password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify({"error": "Invalid email or password"}), 401
        
        # Create user session (simplified - we'll use user ID in frontend)
        return jsonify({
            "message": "Login successful!",
            "user_id": str(user['_id']),
            "email": user['email'],
            "daily_uploads": user['daily_uploads'],
            "plan": user.get('plan', 'free')
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500   

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

