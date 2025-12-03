import requests

RENDER_URL = "https://docreader-i4gx.onrender.com"

print("🔒 Testing Protected Upload")
print("=" * 50)

# Step 1: Login to get user_id
print("1. Logging in...")
login_data = {
    "email": "test@example.com",
    "password": "test123"
}

login_response = requests.post(f"{RENDER_URL}/api/login", json=login_data)
if login_response.status_code != 200:
    print(f"   ❌ Login failed: {login_response.text}")
    exit()

user_data = login_response.json()
user_id = user_data["user_id"]
print(f"   ✅ Logged in as {user_data['email']}")
print(f"   User ID: {user_id}")
print(f"   Daily uploads: {user_data['daily_uploads']}")

# Step 2: Try upload WITHOUT user_id (should fail)
print("\n2. Testing upload without authentication...")
files = {'file': open('sample.pdf', 'rb')}  # Replace with actual test PDF
response = requests.post(f"{RENDER_URL}/analyze", files=files)
print(f"   Response: {response.status_code} - {response.json().get('error', 'No error')}")

# Step 3: Try upload WITH user_id (should work)
print("\n3. Testing upload with authentication...")
files = {'file': open('sample.pdf', 'rb')}
data = {'user_id': user_id}
response = requests.post(f"{RENDER_URL}/analyze", files=files, data=data)
print(f"   Response: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print(f"   ✅ Upload successful!")
    print(f"   Document ID: {result.get('document_id')}")
    print(f"   Rate limit: {result.get('rate_limit_info')}")
else:
    print(f"   Error: {response.text}")

print("\n" + "=" * 50)
print("Test complete!")