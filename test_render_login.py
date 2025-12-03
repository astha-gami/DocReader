import requests

RENDER_URL = "https://docreader-i4gx.onrender.com"

print("🔐 Testing Login on Render")
print("=" * 50)

# Use the user you just registered
login_data = {
    "email": "render_user@example.com",
    "password": "test123"
}

try:
    response = requests.post(f"{RENDER_URL}/api/login", 
                            json=login_data,
                            timeout=10)
    
    if response.status_code == 200:
        print("✅ Login successful on Render!")
        user_data = response.json()
        print(f"User ID: {user_data.get('user_id')}")
        print(f"Email: {user_data.get('email')}")
        print(f"Daily uploads: {user_data.get('daily_uploads')}")
    else:
        print(f"⚠️ Login failed: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")