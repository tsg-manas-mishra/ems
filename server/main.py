from fastapi import FastAPI, Depends, HTTPException, Query
from utils import authUser, decode_token
from models import User
from db import mycollection
from typing import Optional
from pydantic import EmailStr
from core import add_Employee, delEmployee, searchEmp
app = FastAPI()

@app.post("/login/")
async def login(user: User):
    """
    Authenticate user and return a token.
    """
    return await authUser(user)

# Admin dashboard
@app.get("/admin-dashboard/", dependencies=[Depends(decode_token)])
def admin_dashboard():
    try:
        return {"message": "Welcome to the Admin Dashboard"}
    except Exception as e:
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")

#Add Employee
@app.post("/admin-dashboard/add",dependencies=[Depends(decode_token)])
def addingEmployee(user:User):
    try:
        return add_Employee(user)
    except Exception as e:
        raise HTTPException(status_code=500, details=f"Server error {e}")


# Employee dashboard
@app.get("/employee-dashboard/", dependencies=[Depends(decode_token)])
def employee_dashboard(payload: dict = Depends(decode_token)):
    role = payload.get("role")
    if role != "Employee":
        raise HTTPException(status_code=403,detail="Access Forbidden")
    return {"message": "Welcome to the Employee Dashboard"}

#Delete Employee
@app.delete("/delete-employee",dependencies=[Depends(decode_token)])
def deletingemp(email: EmailStr = Query(...)):
    try:
        return delEmployee(email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error {e}")

#Search Employee
@app.get("/search-employee",dependencies=[Depends(decode_token)])
def searchingemp(name: Optional[str] = Query(None), designation: Optional[str] = Query(None),department: Optional[str]=Query(None)):
    try:
        return searchEmp(name,designation,department)
    except:
        raise HTTPException(status_code=500, details="Internal server error")