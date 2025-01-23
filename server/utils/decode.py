from datetime import datetime
from jwt import JWT, jwk_from_dict
from dotenv import load_dotenv
import os
from fastapi import HTTPException, Request

load_dotenv()
instance = JWT()
secret_key = os.getenv("JWT_SECRET")
algo = os.getenv("JWT_ALGORITHM")
def decode_token(request: Request):
    try:
        if not request.headers['authorization']:
            raise HTTPException(status_code=401, detail = "Authorization header is missing")
        if not request.headers['authorization'].startswith("Bearer"):
            raise HTTPException(status_code=401, detail="Invalid header format")
        token: str = request.headers['authorization'].split("Bearer ")[-1]
        # Create a JWK object from the secret key
        try:
            key = jwk_from_dict({"kty": "oct", "k": secret_key})

            # Decode the token
            payload = instance.decode(token, key, do_time_check=True, algorithms=[algo])

            # Validate the expiration time (optional, as `do_time_check` already checks it)
            exp = payload.get("exp")
            if exp and datetime.fromtimestamp(exp) < datetime.now():
                raise HTTPException(status_code=401, detail="Token has expired")
            return payload
        except Exception as e:
            raise HTTPException(status_code=401,detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"There is an error {e}")
        
