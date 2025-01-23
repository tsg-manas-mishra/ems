# from fastapi import FastAPI, Depends, HTTPException
# from utils import authUser, decode_token, role_verify
# from models import User
# from pydantic import EmailStr
# from core import add_Employee,delEmployee
# app = FastAPI()

# @app.post("/login/")
# async def login(user: User):
#     """
#     Authenticate user and return a token.
#     """
#     return await authUser(user)

# # Admin dashboard
# # @app.get("/admin-dashboard/", dependencies=[Depends(role_verify(["Admin"]))])
# @app.get("/admin-dashboard",)
# def admin_dashboard():
#     return {"message": "Welcome to the Admin Dashboard"}

# #Add Employee
# @app.post("/admin-dashboard/add",dependencies=[Depends(decode_token)])
# def addingEmployee(user:User):
#     """
#     Adding an employee
#     """
#     try:
#         return add_Employee(user)
#     except Exception as e:
#         raise HTTPException(status_code=500, details=f"Server error {e}")

    
# # Employee dashboard
# @app.get("/employee-dashboard/", dependencies=[Depends(decode_token)])
# def employee_dashboard(curr: dict = Depends(decode_token)):
#     if curr.get("role") != "Employee":
#         raise HTTPException(status_code=403, detail="Access forbidden: Employees only")
#     return {"message": "Welcome to the Employee Dashboard"}


from fastapi import FastAPI, Depends, HTTPException, Query
from utils import authUser, decode_token
from models import User
from pydantic import EmailStr
from core import add_Employee, delEmployee
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
def employee_dashboard(curr: dict = Depends(decode_token)):
    return {"message": "Welcome to the Employee Dashboard"}

#Delete Employee
@app.delete("/delete-employee",dependencies=[Depends(decode_token)])
def deletingemp(email: EmailStr = Query(...)):
    try:
        return delEmployee(email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error {e}")