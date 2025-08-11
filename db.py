from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()  # 讀取 .env

client = MongoClient(os.getenv("MONGO_URI"))
db = client["chinapress"]