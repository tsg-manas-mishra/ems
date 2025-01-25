from fastapi import HTTPException,Depends
from utils import decode_token
from db import user_collection
from pydantic import EmailStr

def delEmployee(EM: EmailStr,payload: dict=Depends(decode_token)):
    # check if the payload has email ID
    email = payload["email"]
    if not email:
        raise HTTPException(status_code=400, detail="Email ID missing") 
    # check if the payload is admin
    role = payload["role"]
    if role!= "Admin":
        raise HTTPException(status_code=403, detail="Forbidden access, Admin Only")
    # Check if the employee exists
    existing_employee = user_collection.find_one({"email": EM})
    if not existing_employee:
        raise HTTPException(status_code=404, detail="Email ID does not exist")  # Use 404 for "Not Found"
    
    try:
        # Delete the employee
        deleted_employee = user_collection.find_one_and_delete({"email": EM})
        if deleted_employee:
            return {"message": "Employee Deleted Successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete employee")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {e}")