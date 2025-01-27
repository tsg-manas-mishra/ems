from fastapi import FastAPI, Depends, HTTPException, Query
from utils import authUser, decode_token
from models import User, UpdateEmployee
from typing import Optional
from pydantic import EmailStr
from core import add_Employee, delEmployee, searchEmp, update_employee
from api import admin_dashboard, employee_dashboard
app = FastAPI()

@app.post("/login/")
def login(user: User):
    """
    Authenticate user and return a token.
    """
    return authUser(user)

# Admin dashboard
@app.get("/admin-dashboard/", dependencies=[Depends(decode_token)])
def admindashboard(payload:dict=Depends(decode_token)):
    try:
        return admin_dashboard(payload)
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")

#Add Employee
@app.post("/admin-dashboard/add", dependencies=[Depends(decode_token)])
def addingEmployee(user: User, payload: dict = Depends(decode_token)):
    try:
        # Pass the payload (decoded token) to add_Employee
        return add_Employee(user, payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error {e}")


# Employee dashboard
@app.get("/employee-dashboard/", dependencies=[Depends(decode_token)])
def employeedashboard(payload:dict=Depends(decode_token)):
    try:
        return employee_dashboard(payload)
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")

#Delete Employee
@app.delete("/delete-employee/{email}",dependencies=[Depends(decode_token)])
def deletingemp(email:EmailStr,payload: dict=Depends(decode_token)):
    try:
        return delEmployee(email,payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error {e}")

#Search Employee
@app.get("/search-employee",dependencies=[Depends(decode_token)])
def searchingemp(email: Optional[EmailStr] = Query(None), designation: Optional[str] = Query(None),department: Optional[str]=Query(None)):
    try:
        return searchEmp(email,designation,department)
    except:
        raise HTTPException(status_code=500, detail="Internal server error")

#Edit Employee
@app.put("/edit-employee/{email}")
def editemp(email: EmailStr, update_data: UpdateEmployee, payload: dict = Depends(decode_token)):
    try:
        return update_employee(email, update_data, payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")    