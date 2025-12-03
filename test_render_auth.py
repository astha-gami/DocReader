# test_render_auth.py
import requests
import json

RENDER_URL = "https://docreader-i4gx.onrender.com"

print("🌐 Testing Render Deployment")
print("=" * 50)

# Test 1: Home page
print("1. Testing home page...")
try:
    response = requests.get(RENDER_URL, timeout=10)
    print(f"   Status: {response.status_code}")
    print(f"   Response (first 100 chars): {response.text[:100]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Registration
print("\n2. Testing registration on Render...")
register_data = {
    "email": "render_user@example.com",
    "password": "test123"
}

try:
    response = requests.post(f"{RENDER_URL}/api/register", 
                            json=register_data,
                            headers={"Content-Type": "application/json"},
                            timeout=15)
    
    if response.status_code == 201:
        print(f"   ✅ Registration working on Render!")
        print(f"   User ID: {response.json().get('user_id')}")
    elif response.status_code == 500:
        print(f"   🔧 Server error - check Render logs")
        print(f"   Error: {response.text[:200]}")
    else:
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        
except Exception as e:
    print(f"   ❌ Connection failed: {e}")

print("\n" + "=" * 50)
print("If registration works, your deployment is successful!")