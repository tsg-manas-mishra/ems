from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from models import User
from passlib.context import CryptContext
from core.isExists import checkIfExists
from db import user_collection, update_collection
from utils import decode_token
import datetime

def add_Employee(user: User, payload: dict = Depends(decode_token)):
    role = payload.get("role")
    
    # If there is no role in the payload
    if not role:
        return JSONResponse(status_code=401, content={"message": "Bad Request"})
    
    # If the role is anything other than admin
    if role != "Admin":
        return JSONResponse(status_code=403, content={"message": "Forbidden access"})
    
    # To check if email already exists and deny access
    if(checkIfExists(user.email)):
        return JSONResponse(status_code=409, content={"message": "User already exists"})


    entry = user.model_dump()
    hashing = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = hashing.hash(entry["password"])
    entry["password"] = hashed_password
    entry["Joining_Date"] = datetime.datetime.now()

    try:
        user_collection.insert_one(entry)
        entry["updated"] = datetime.datetime.now()
        del entry["Joining_Date"]
        update_collection.insert_one(entry)
        return {"message": "Employee added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while adding employee: {e}")
