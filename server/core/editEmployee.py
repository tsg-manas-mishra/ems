from db import user_collection, redis_client
from fastapi.responses import JSONResponse
from pydantic import EmailStr
from models import UpdateEmployee
from datetime import datetime

def update_employee(email: EmailStr, update_data: UpdateEmployee, token_payload: dict):
    role = token_payload.get("role")
    token_email = token_payload.get("email")

    if not token_email:
        raise JSONResponse(status_code=401, content="Log in again")

    #Fetch the employee record from MongoDB
    employee = user_collection.find_one({"email": email})
    if not employee:
        raise JSONResponse(status_code=404, content="Employee not found")

    #Determine allowed fields based on role
    if role == "Employee":
        if token_email != email:
            raise JSONResponse(status_code=403, content="Access forbidden")
        allowed_fields = {"contact", "address"}
    elif role == "Admin":
        allowed_fields = {"name", "designation", "department", "contact", "address"}
    else:
        raise JSONResponse(status_code=403, detail="Access forbidden")

    ##Filter update_data
    update_data = {
        field: value
        for field, value in update_data.model_dump(exclude_unset=True).items()
        if field in allowed_fields
    }
    if not update_data:
        raise JSONResponse(status_code=400, content="No valid fields to update")

    #Validate and convert contact field
    if "contact" in update_data and isinstance(update_data["contact"], str):
        try:
            update_data["contact"] = int(update_data["contact"])
        except ValueError:
            raise JSONResponse(status_code=400, content="Invalid contact value: must be a valid integer")

    #Update MongoDB document
    update_result = user_collection.update_one({"email": email}, {"$set": {**update_data, "updated": datetime.now()}})
    if update_result.matched_count == 0:
        raise JSONResponse(status_code=400, content="Failed to update employee")

    #Remove outdated employee data from Redis
    redis_key = f"user:{email}"
    redis_client.delete(redis_key)  # Deletes the hash key from Redis

# Fetch updated employee from MongoDB and re-cache
    updated_employee = user_collection.find_one({"email": email})
    if updated_employee:
        updated_employee["_id"] = str(updated_employee["_id"])
        updated_employee.pop("password", None)
        updated_employee.pop("Joining_Date", None)

        # Store updated data in Redis
        redis_client.hset(redis_key, mapping={
            "_id": updated_employee["_id"],
            "name": updated_employee["name"],
            "email": updated_employee["email"],
            "role": updated_employee.get("role", ""),
            "department": updated_employee.get("department", ""),
            "designation": updated_employee.get("designation", ""),
            "address": updated_employee.get("address", ""),
            "contact": str(updated_employee.get("contact", "")),
            "updated": str(updated_employee["updated"])
        })
        redis_client.expire(redis_key, 600)  # Set expiry to 10 minutes