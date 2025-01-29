from fastapi import HTTPException
from models import User
from pymongo.errors import PyMongoError
from utils.auth import create_access_token
from db import user_collection
from passlib.context import CryptContext

# Password hashing context
context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authUser(user: User):
    """Authenticating the user and returning a token"""
    try:
        # Fetch user by email from the database
        db_user = user_collection.find_one({"email": user.email})

        if not db_user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Verify the password
        if not context.verify(user.password, db_user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Create token payload with essential details
        token_data = {"email": db_user.get("email"),"role": db_user.get("role")}

        # Generate access token
        access_token = create_access_token(token_data)

        return {"access_token": access_token, "token_type": "Bearer", "role":db_user.get("role"), "name":db_user.get("name")}

    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
