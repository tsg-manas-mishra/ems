from fastapi import HTTPException
from models import User
from pymongo.errors import PyMongoError
from utils.auth import create_access_token
from db import mycollection

async def authUser(user:User):
    "Authenticating the user and return a token"
    try:
        #Retrieve details of the user from the database
        db_user = mycollection.find_one({"email":user.email})
        if not db_user or db_user["password"]!=user.password:
            raise HTTPException(status_code = 401, detail="Invalid email or password")
        #If user found, generate the token
        token_data = {"email":db_user["email"],"password":db_user["password"], "role":db_user["role"]}
        access_token = create_access_token(token_data)
        return {"access_token":access_token,"token_type":"bearer"}
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error:{e}")