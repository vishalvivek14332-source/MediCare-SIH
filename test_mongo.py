import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("MONGO_URI")
if not uri:
    print("MONGO_URI not found")
    sys.exit(1)

print(f"Connecting to: {uri[:40]}...")
try:
    # 5 second timeout
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    info = client.server_info()
    print("Connected successfully!")
except Exception as e:
    print(f"Connection failed: {e}")
