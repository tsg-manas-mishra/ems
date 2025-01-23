from fastapi import HTTPException
from db import mycollection
from pydantic import EmailStr

def delEmployee(EM: EmailStr):
    # Check if the employee exists
    existing_employee = mycollection.find_one({"email": EM})
    if not existing_employee:
        raise HTTPException(status_code=404, detail="Email ID does not exist")  # Use 404 for "Not Found"
    
    try:
        # Delete the employee
        deleted_employee = mycollection.find_one_and_delete({"email": EM})
        if deleted_employee:
            return {"message": "Employee Deleted Successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete employee")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {e}")