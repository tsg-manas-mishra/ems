from fastapi import FastAPI
from utils.token_verify import authUser
from models import User
app = FastAPI()

@app.post("/login/")
async def login(user: User):
    """
    Authenticate user and return a token.
    """
    return await authUser(user)
