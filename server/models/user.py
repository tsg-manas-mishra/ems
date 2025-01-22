from pydantic import BaseModel, EmailStr
class User(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: str
    contact: int

# class Token(BaseModel):
#     access_token: str
#     token_type: str
