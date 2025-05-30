import os
import urllib.parse
from pymongo import MongoClient

MONGO_HOST = os.getenv("MONGO_HOST", "mongo")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "mydatabase")
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

if MONGO_USERNAME and MONGO_PASSWORD:
    user = urllib.parse.quote_plus(MONGO_USERNAME)
    password = urllib.parse.quote_plus(MONGO_PASSWORD)
    uri = f"mongodb://{user}:{password}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DATABASE}?authSource=admin"
else:
    uri = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DATABASE}"

client = MongoClient(uri)

def get_db():
    yield client[MONGO_DATABASE]
