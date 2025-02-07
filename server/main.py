from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import  JSONResponse
from utils import authUser, decode_token
from models import User, UpdateEmployee
from typing import Optional
from pydantic import EmailStr
from core import add_Employee, delEmployee, searchEmp, update_employee, get_all_users_service
app = FastAPI()

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login/")
def login(user: User):
    """
    Authenticate user and return a token.
    """
    return authUser(user)

# Admin dashboard
@app.get("/dashboard/")
def dashboard(payload: dict = Depends(decode_token)):
    role = payload.get("role")
    if role == "Admin":
        return {"message": "Welcome, Admin!"}
    elif role == "Employee":
        return {"message": "Welcome, Employee!"}
    else:
        raise JSONResponse(status_code=403, content="Access denied")

# fetch all users
@app.get("/users/")
def get_all_users(
    column: Optional[str] = Query(None), 
    order: Optional[str] = Query("asc"),
    payload: dict = Depends(decode_token)
):  
    return get_all_users_service(column, order,payload)

#Add_Employee
@app.post("/add")
def addingEmployee(user: User, payload: dict = Depends(decode_token)):
    try:
        # Pass the payload (decoded token) to add_Employee
        return add_Employee(user, payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error {e}")


#Delete__Employee
@app.delete("/delete-employee/{email}")
def deletingemp(email:EmailStr,payload: dict=Depends(decode_token)):
    try:
        return delEmployee(email,payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error {e}")

#Search_Employee
@app.get("/search-employee/",dependencies=[Depends(decode_token)])
def searchingemp(name: Optional[str] = Query(None), designation: Optional[str] = Query(None),department: Optional[str]=Query(None)):
    try:
        return searchEmp(name,designation,department)
    except:
        raise HTTPException(status_code=500, detail="Internal server error")

#Edit Employee
@app.put("/edit-employee/{email}")
def editemp(email: EmailStr, update_data: UpdateEmployee, payload: dict = Depends(decode_token)):
    try:
        return update_employee(email, update_data, payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")    