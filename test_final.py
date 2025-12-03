# test_final.py
print("📊 MongoDB Setup Test - Day 1")
print("=" * 50)

# PASTE YOUR CONNECTION STRING HERE
CONN = "mongodb+srv://asthagami2707_db_user:ZiNSWzq6cW79XDuD@cluster0.hypc9k3.mongodb.net/?appName=Cluster0"

print(f"Testing connection to: {CONN[:50]}...")

try:
    from pymongo import MongoClient
    print("1. Import successful!")
    
    client = MongoClient(CONN)
    print("2. Client created!")
    
    # Test 1: Ping
    print("3. Testing connection (ping)...")
    client.admin.command('ping')
    print("   ✅ Connected to MongoDB!")
    
    # Test 2: List DBs
    print("4. Checking databases...")
    dbs = client.list_database_names()
    print(f"   Found {len(dbs)} databases")
    
    # Test 3: Create test data
    print("5. Creating test document...")
    db = client["docreader_main"]
    col = db["day1_test"]
    
    doc = {
        "test": "success", 
        "day": 1, 
        "app": "Document Analyzer",
        "message": "MongoDB is working!"
    }
    
    result = col.insert_one(doc)
    print(f"   ✅ Document inserted! ID: {result.inserted_id}")
    
    # Count documents
    count = col.count_documents({})
    print(f"6. Total test documents: {count}")
    
    print("=" * 50)
    print("🎉 DAY 1 COMPLETE!")
    print("MongoDB is ready for your Document Analyzer app!")
    print("\nTomorrow: Add user registration to your Flask app!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n🔧 Troubleshooting:")
    print("1. Run: pip install pymongo")
    print("2. Check IP Access List has 0.0.0.0/0")
    print("3. Wait 1 minute after adding IP address")
    print("4. Verify password in connection string")