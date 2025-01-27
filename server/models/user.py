from pydantic import BaseModel, EmailStr
from datetime import date
class User(BaseModel):
    email: EmailStr = None
    password: str = None
    name: str = None
    role: str = None
    contact: int=None
    designation: str = None
    department: str = None
    address: str = None
    Joining_Date: date = None