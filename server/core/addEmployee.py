from fastapi import HTTPException
from models import User
from passlib.context import CryptContext
from db import mycollection

def add_Employee(user:User):
    entry = user.dict()
    hashing = CryptContext(schemes=["bcrypt"])
    hashed_password = hashing.hash(entry["password"])
    entry["password"] =hashed_password
    try:
        mycollection.insert_one(entry)
        return {"message": "Employee added successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error is {e}")
