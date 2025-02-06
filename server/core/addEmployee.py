from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from models import User
from passlib.context import CryptContext
from core.isExists import checkIfExists
from db import user_collection, update_collection, redis_client
from utils import decode_token
import datetime
import json

def add_Employee(user: User, payload: dict = Depends(decode_token)):
    role = payload.get("role")
    
    # If there is no role in the payload
    if not role:
        return JSONResponse(status_code=401, content={"message": "Bad Request"})
    
    # If the role is anything other than admin
    if role != "Admin":
        return JSONResponse(status_code=403, content={"message": "Forbidden access"})
    
    # To check if email already exists and deny access
    if checkIfExists(user.email):
        return JSONResponse(status_code=409, content={"message": "User already exists"})

    entry = user.model_dump()
    entry["email"] = user.email  # Ensure email is explicitly added

    hashing = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = hashing.hash(entry["password"])
    entry["password"] = hashed_password
    entry["Joining_Date"] = datetime.datetime.now()

    try:
        # Insert into MongoDB
        user_collection.insert_one(entry)
        entry["updated"] = datetime.datetime.now()
        del entry["Joining_Date"]
        update_collection.insert_one(entry)

        # Convert MongoDB ObjectId and datetime fields
        entry["_id"] = str(entry["_id"])
        entry["updated"] = str(entry["updated"])

        # **1️⃣ Store the new employee in Redis Hash (`HSET user:{email}`)**
        redis_key = f"user:{user.email}"
        redis_client.hset(redis_key, mapping={
            "_id": entry["_id"],
            "name": entry["name"],
            "email": entry["email"],  # Ensure email is stored
            "role": entry["role"],
            "department": entry["department"],
            "designation": entry["designation"],
            "address": entry["address"],
            "contact": entry["contact"],
            "updated": entry["updated"]
        })

        redis_client.expire(redis_key, 600)

        # **2️⃣ Update "all_users" Redis Hash Instead of JSON**
        redis_client.hset("all_users", entry["email"], json.dumps({
            "_id": entry["_id"],
            "name": entry["name"],
            "email": entry["email"],
            "role": entry["role"],
            "department": entry["department"],
            "designation": entry["designation"],
            "address": entry["address"],
            "contact": entry["contact"],
            "updated": entry["updated"]
        }))

        redis_client.expire("all_users", 600)  # Set expiry for 10 minutes

        return {"message": "Employee added successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while adding employee: {e}")
