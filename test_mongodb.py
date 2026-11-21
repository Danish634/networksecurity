import os
from pymongo import MongoClient
from dotenv import load_dotenv
import certifi

load_dotenv()

uri = os.getenv("MONGO_DB_URL")

client = None

try:
    client = MongoClient(
        uri,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=10000
    )

    client.admin.command("ping")

    print("Connected successfully!")

except Exception as e:
    print("MongoDB connection failed:", e)

finally:
    if client:
        client.close()
