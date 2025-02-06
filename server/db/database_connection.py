from pymongo import MongoClient
from dotenv import load_dotenv
import os,redis
# Load environment variables
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
load_dotenv(dotenv_path)

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

# Select database and collection
redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    password=os.getenv("REDIS_PASSWORD"),
    ssl=os.getenv("REDIS_SSL", "True") == "True",  # Ensure it's a boolean
    decode_responses=True
)
mydatabase = client["ems"]
user_collection = mydatabase["users"]
update_collection = mydatabase["update"]
