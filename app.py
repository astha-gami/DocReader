# === ADD THESE IMPORTS ===
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId  # ← ADD THIS LINE
import bcrypt
from ai_engine.engine import analyze_document
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
MONGO_URI = os.getenv('MONGO_URI') 

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["docreader_db"]  # Database name
users_collection = db["users"]  # Collection for user accounts
documents_collection = db["documents"]  # Collection for uploaded documents

print("✅ Connected to MongoDB!")
# ====================================

# ====================================

# ========== DAY 3: HELPER FUNCTIONS ==========
def check_rate_limit(user_id):
    """Check if user has reached daily upload limit (10/day for free users)"""
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        
        if not user:
            return False, "User not found"
        
        # Reset counter if it's a new day
        last_reset = user.get('last_reset', datetime.utcnow())
        today = datetime.utcnow().date()
        
        if last_reset.date() < today:
            # Reset daily counter
            users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"daily_uploads": 0, "last_reset": datetime.utcnow()}}
            )
            user['daily_uploads'] = 0
        
        # Check limit (10 for free users)
        plan = user.get('plan', 'free')
        limit = 10 if plan == 'free' else 1000  # 1000 for premium (future)
        
        current_uploads = user.get('daily_uploads', 0)
        if current_uploads >= limit:
            return False, f"Daily limit reached ({current_uploads}/{limit} uploads). Upgrade plan for more."
        
        return True, f"OK ({current_uploads}/{limit} used today)"
        
    except Exception as e:
        return False, f"Error checking rate limit: {str(e)}"

def update_upload_count(user_id):
    """Increment user's daily upload count"""
    try:
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$inc": {"daily_uploads": 1}}
        )
        return True
    except Exception as e:
        print(f"Error updating upload count: {e}")
        return False

def save_document_to_db(user_id, filename, analysis_result, raw_text=""):
    """Save analyzed document to database"""
    try:
        document_data = {
            "user_id": ObjectId(user_id),
            "filename": filename,
            "upload_date": datetime.utcnow(),
            "extracted_data": analysis_result,
            "raw_text": raw_text,
            "file_size": os.path.getsize(os.path.join(app.config["UPLOAD_FOLDER"], filename)) if os.path.exists(os.path.join(app.config["UPLOAD_FOLDER"], filename)) else 0
        }
        
        result = documents_collection.insert_one(document_data)
        return str(result.inserted_id)
    except Exception as e:
        print(f"Error saving document to DB: {e}")
        return None
# =============================================
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
def landing():
    return render_template("landing.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/register") 
def register_page():
    return render_template("register.html")



# ----------------------
# PDF ANALYZE API (PROTECTED)
# ----------------------
@app.route("/analyze", methods=["POST"])
def analyze_file():
    # 1. Check if user is authenticated
    user_id = request.form.get('user_id')
    
    if not user_id:
        return jsonify({"error": "Authentication required. Please login first."}), 401
    
    # 2. Verify user exists
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"error": "Invalid user. Please login again."}), 401
    except:
        return jsonify({"error": "Invalid user ID format."}), 400
    
    # 3. Check rate limit
    allowed, message = check_rate_limit(user_id)
    if not allowed:
        return jsonify({"error": message}), 429  # 429 = Too Many Requests
    
    # 4. Check if file is included
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # 5. Save uploaded PDF
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    try:
        # 6. Run your AI engine (keep your existing function)
        result = analyze_document(file_path)
        
        # 7. Save document to database
        doc_id = save_document_to_db(
            user_id=user_id,
            filename=file.filename,
            analysis_result=result
        )
        
        # 8. Update user's upload count
        update_upload_count(user_id)
        
        # 9. Add document ID to response
        result["document_id"] = doc_id
        result["user_id"] = user_id
        result["rate_limit_info"] = message
        
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # 10. Cleanup: Delete uploaded file after processing
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass

# ----------------------
# GET USER'S DOCUMENT HISTORY
# ----------------------
@app.route("/api/documents", methods=["GET"])
def get_user_documents():
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"error": "User ID required"}), 400
    
    try:
        # Get documents for this user, newest first
        documents = list(documents_collection.find(
            {"user_id": ObjectId(user_id)},
            {"_id": 1, "filename": 1, "upload_date": 1, "extracted_data": 1}
        ).sort("upload_date", -1).limit(50))
        
        # Convert ObjectId to string
        for doc in documents:
            doc["_id"] = str(doc["_id"])
            doc["user_id"] = str(doc.get("user_id", ""))
        
        return jsonify({
            "count": len(documents),
            "documents": documents
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# ----------------------
# GET USER PROFILE/STATS
# ----------------------
@app.route("/api/user", methods=["GET"])
def get_user_info():
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"error": "User ID required"}), 400
    
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Get document count
        doc_count = documents_collection.count_documents({"user_id": ObjectId(user_id)})
        
        return jsonify({
            "user_id": str(user["_id"]),
            "email": user["email"],
            "created_at": user["created_at"].isoformat() if isinstance(user["created_at"], datetime) else str(user["created_at"]),
            "daily_uploads": user.get("daily_uploads", 0),
            "plan": user.get("plan", "free"),
            "total_documents": doc_count,
            "last_reset": user.get("last_reset", "").isoformat() if isinstance(user.get("last_reset"), datetime) else str(user.get("last_reset", ""))
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500    

# ----------------------
# RUN SERVER
# ----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

