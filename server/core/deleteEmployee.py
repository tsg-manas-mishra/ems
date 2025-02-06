from fastapi import HTTPException, Depends
from utils import decode_token
from fastapi.responses import JSONResponse
from db import user_collection, redis_client
from pydantic import EmailStr

def delEmployee(EM: EmailStr, payload: dict = Depends(decode_token)):
    """
    Delete an employee from MongoDB and remove their data from Redis.
    """
    email = payload.get("email")
    role = payload.get("role")

    if not email:
        raise JSONResponse(status_code=400, content={"detail": "Email ID missing"}) 

    if role != "Admin":
        raise JSONResponse(status_code=403, content={"detail": "Forbidden"})

    # Check if the employee exists
    existing_employee = user_collection.find_one({"email": EM})
    if not existing_employee:
        raise JSONResponse(status_code=404, content={"detail": "Email ID does not exist"})  
    
    try:
        # **Delete the employee from MongoDB**
        deleted_employee = user_collection.find_one_and_delete({"email": EM})
        if not deleted_employee:
            raise HTTPException(status_code=500, detail="Failed to delete employee")

        # **Remove Employee from Redis**
        redis_key = f"user:{EM}"
        redis_client.delete(redis_key)  # Remove the user's hash key

        # **Invalidate "all_users" Cache**
        redis_client.delete("all_users")  # Ensures fresh data is loaded on next request

        return {"message": "Employee Deleted Successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {e}")
