from fastapi import FastAPI, Depends, HTTPException, Query
from utils import authUser, decode_token
from models import User, UpdateEmployee
from db import user_collection,update_collection
from typing import Optional
from pydantic import EmailStr
from core import add_Employee, delEmployee, searchEmp
from api import admin_dashboard, employee_dashboard
app = FastAPI()

@app.post("/login/")
async def login(user: User):
    """
    Authenticate user and return a token.
    """
    return await authUser(user)

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
def searchingemp(name: Optional[str] = Query(None), designation: Optional[str] = Query(None),department: Optional[str]=Query(None)):
    try:
        return searchEmp(name,designation,department)
    except:
        raise HTTPException(status_code=500, details="Internal server error")

#Edit Employee
@app.put("/edit-employee/{email}", dependencies=[Depends(decode_token)])
def update_employee(email: EmailStr,update_data: UpdateEmployee,payload: dict = Depends(decode_token)):
    """
    Handles employee and admin updates
    Admins can update all fields except email.
    Employees can update only phone_number and address.
    """
    # Extract role and email from the token payload
    role = payload.get("role")
    token_email = payload.get("email")

    if not token_email:
        raise HTTPException(status_code=401, detail="Invalid token: Email missing")

    employee = user_collection.find_one({"email": email})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Validate role-based permissions
    if role == "Employee":
        if token_email != email:
            raise HTTPException(status_code=403, detail="Access forbidden: Employees can only update their own record")
        
        # Allow employees to update only phone_number and address
        allowed_fields = {"contact", "address"}
        update_data = {field: value for field, value in update_data.dict(exclude_unset=True).items() if field in allowed_fields}

    elif role == "Admin":
        # Admins can update all fields except email
        if "email" in update_data.dict(exclude_unset=True):
            raise HTTPException(status_code=400, detail="Admins cannot update the email field")
        
        # Allow admins to update all fields except email
        allowed_fields = {"name", "designation", "department", "contact", "address"}
        update_data = {field: value for field, value in update_data.dict(exclude_unset=True).items() if field in allowed_fields}
    else:
        raise HTTPException(status_code=403, detail="Access forbidden: Invalid role")

    # Perform the update in the database
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")

    update_result = user_collection.update_one(
        {"email": email},
        {"$set": update_data}
    )

    if update_result.matched_count == 0:
        raise HTTPException(status_code=400, detail="Failed to update employee")

    # Return the updated employee details
    updated_employee = user_collection.find_one({"email": email})
    updated_employee["_id"] = str(updated_employee["_id"])  # Convert ObjectId to string for JSON serialization

    return {
        "message": "Employee updated successfully",
        "updated_employee": updated_employee
    }