from fastapi import FastAPI, Depends, HTTPException
from utils import authUser, decode_token
from models import User
from core import add_Employee
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


# Employee dashboardg
@app.get("/employee-dashboard/", dependencies=[Depends(decode_token)])
def employee_dashboard(curr: dict = Depends(decode_token)):
    if curr.get("role") != "Employee":
        raise HTTPException(status_code=403, detail="Access forbidden: Employees only")
    return {"message": "Welcome to the Employee Dashboard"}