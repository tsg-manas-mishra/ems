from fastapi import HTTPException
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from jwt import (
    JWT,
    jwk_from_dict,
)


instance = JWT()

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
load_dotenv(dotenv_path)
JWT_SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES"))

def create_access_token(data: dict):
    if data is None:
        raise HTTPException(status_code=401,detail="Data to encode is missing")
    try:
        # Create a copy of the data to avoid modifying the original dictionary
        to_encode = data.copy()
        
        # Add expiration time to the payload
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": int(expire.timestamp())})
        
        # Create a JWK object from the secret key
        key = jwk_from_dict({"kty": "oct", "k": JWT_SECRET_KEY})
        
        # Encode the token
        token = instance.encode(payload=to_encode, key=key, alg=ALGORITHM)
        return token
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"database error {e}")