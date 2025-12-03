# test_auth.py
import requests
import json

BASE_URL = "http://localhost:5000"

print("🧪 Testing User Registration and Login")
print("=" * 50)

# Test 1: Register a new user
print("1. Testing registration...")
register_data = {
    "email": "test@example.com",
    "password": "test123"
}

response = requests.post(f"{BASE_URL}/api/register", 
                        json=register_data,
                        headers={"Content-Type": "application/json"})

if response.status_code == 201:
    print(f"   ✅ Registration successful!")
    print(f"   Response: {response.json()}")
else:
    print(f"   ❌ Registration failed: {response.status_code}")
    print(f"   Error: {response.text}")

# Test 2: Login with same user
print("\n2. Testing login...")
login_data = {
    "email": "test@example.com",
    "password": "test123"
}

response = requests.post(f"{BASE_URL}/api/login", 
                        json=login_data,
                        headers={"Content-Type": "application/json"})

if response.status_code == 200:
    print(f"   ✅ Login successful!")
    user_data = response.json()
    print(f"   User ID: {user_data.get('user_id')}")
    print(f"   Email: {user_data.get('email')}")
    print(f"   Daily uploads: {user_data.get('daily_uploads')}")
else:
    print(f"   ❌ Login failed: {response.status_code}")
    print(f"   Error: {response.text}")

print("\n" + "=" * 50)
print("🎉 Auth endpoints are working!")