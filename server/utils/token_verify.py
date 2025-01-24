from fastapi import HTTPException
from models import User
from pymongo.errors import PyMongoError
from utils.auth import create_access_token
from db import mycollection
from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

async def authUser(user:User):
    "Authenticating the user and return a token"
    try:
        #Retrieve details of the user from the database

        db_user = mycollection.find_one({"email":user.email,"role":user.role})
        if not db_user:
            raise HTTPException(status_code = 401, detail="Invalid email or password")
        if not context.verify(user.password,db_user["password"]):
            raise HTTPException(status_code=403,details="Invalid email or password")
        token_data = {"email":db_user["email"],"role":db_user["role"]}
        access_token = create_access_token(token_data)
        return {"access_token":access_token,"token_type":"Bearer"}
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error:{e}")