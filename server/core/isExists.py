from fastapi import HTTPException
from db import user_collection
from pydantic import EmailStr

def checkIfExists(email: EmailStr):
    """
    Check if an employee already exists in the database.
    Raises HTTP 409 if found.
    """
    db_user = user_collection.find_one({"email": email})
    if db_user:
        return True
    return False