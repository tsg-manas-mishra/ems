from pydantic import BaseModel, EmailStr
class User(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: str
    contact: int
    designation: str
    department: str
    address: str

# class Token(BaseModel):
#     access_token: str
#     token_type: str
