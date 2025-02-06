from fastapi import Depends, HTTPException
from typing import Optional
from db import user_collection, redis_client
from utils import decode_token
from datetime import datetime
import json


def get_all_users_service(column: Optional[str] = None, order: Optional[str] = "asc", payload: dict = Depends(decode_token)):
    """
    Fetch all users with optional sorting and Redis caching using "all_users" as the main key.
    """
    try:
        allowed_columns = ["name", "email", "role", "department", "designation", "address", "contact"]

        if column and column not in allowed_columns:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid column '{column}'. Allowed: {allowed_columns}",
            )

        # Fetch all users from the Redis hash "all_users"
        users_dict = redis_client.hgetall("all_users")
        users = []

        if users_dict:
            print("Fetching users from Redis cache")
            for email, user_data in users_dict.items():
                users.append(json.loads(user_data))  # Convert JSON string back to dictionary
        
        # If Redis is empty, fetch from MongoDB
        if not users:
            print("Fetching from database as data is not in Redis")
            query = {}
            users = list(user_collection.find(query, {"password": 0}))

            # Convert MongoDB data to JSON serializable format
            for user in users:
                user["_id"] = str(user["_id"])  # Convert ObjectId to string
                user = serialize_mongo_data(user)

                # Store user data in Redis Hash (`HSET all_users {email} {user_data}`)
                redis_client.hset("all_users", user["email"], json.dumps(user))

            redis_client.expire("all_users", 600)  # Set expiry (10 min)

        # Apply sorting if required
        if column:
            users.sort(key=lambda x: x.get(column, ""), reverse=(order == "desc"))

        return users

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


def serialize_mongo_data(data):
    """
    Converts MongoDB objects (including datetime) to JSON serializable format.
    """
    if isinstance(data, list):
        return [serialize_mongo_data(doc) for doc in data]
    
    if isinstance(data, dict):
        return {
            key: str(value) if isinstance(value, datetime) else value
            for key, value in data.items()
        }

    return data
