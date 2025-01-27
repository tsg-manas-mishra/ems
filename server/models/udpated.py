from pydantic import BaseModel
from datetime import date
class UpdateEmployee(BaseModel):
    role: str = None
    designation: str = None
    department: str = None
    contact:int = None
    phone_number: str = None
    address: str = None
    updated: date = None