from fastapi import Depends, HTTPException
from models import User
from passlib.context import CryptContext
from db import user_collection
from utils import decode_token
import datetime

def add_Employee(user:User,payload: dict= Depends(decode_token)):
    role = payload["role"]
    # if there is no role in the payload
    if not role:
        raise HTTPException(status_code=400,detail="Invalid token")
    # if the role is anything other than admin
    if role!="Admin":
        raise HTTPException(status_code=403, detail="Forbidden access")
    # to check if email already exists and deny access
    to_add_email = user.email
    count = user_collection.count_documents({"email":to_add_email})
    if count>0:
        raise HTTPException(status_code=403,detail="Can not have more than 1 employee with same Email ID")
    entry = user.dict()
    hashing = CryptContext(schemes=["bcrypt"],deprecated="auto")
    hashing.default_scheme()
    hashed_password = hashing.hash(entry["password"])
    entry["password"] = hashed_password
    entry["Joining_Date"]= datetime.datetime.now()
    try:
        user_collection.insert_one(entry)
        return {"message": "Employee added successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error is {e}")
