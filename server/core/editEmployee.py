from fastapi import HTTPException
from db import user_collection, update_collection
from pydantic import EmailStr
from models import UpdateEmployee
from datetime import datetime

def update_employee(email: EmailStr, update_data: UpdateEmployee, token_payload: dict):
    role = token_payload.get("role")
    token_email = token_payload.get("email")

    if not token_email:
        raise HTTPException(status_code=401, detail="Invalid token: Email missing")

    # Fetch the employee record
    employee = user_collection.find_one({"email": email})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Determine allowed fields based on role
    if role == "Employee":
        if token_email != email:
            raise HTTPException(status_code=403, detail="Access forbidden: Employees can only update their own record")
        allowed_fields = {"contact", "address"}
    elif role == "Admin":
        allowed_fields = {"name", "designation", "department", "contact", "address"}
    else:
        raise HTTPException(status_code=403, detail="Access forbidden: Invalid role")

    # Filter update_data
    update_data = {
        field: value
        for field, value in update_data.dict(exclude_unset=True).items()
        if field in allowed_fields
    }
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")

    # Validate and convert contact field
    if "contact" in update_data and isinstance(update_data["contact"], str):
        try:
            update_data["contact"] = int(update_data["contact"])
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid contact value: must be a valid integer")

    # Update MongoDB document
    update_result = user_collection.update_one({"email": email}, {"$set": {**update_data,"updated":datetime.now()}})
    if update_result.matched_count == 0:
        raise HTTPException(status_code=400, detail="Failed to update employee")

    # Fetch and sanitize the updated employee
    updated_employee = user_collection.find_one({"email": email})
    if updated_employee:
        updated_employee["_id"] = str(updated_employee["_id"])
        updated_employee.pop("password")
        updated_employee.pop("Joining_Date")
    # Add to update collection for audit
    update_collection.insert_one({key: value for key, value in updated_employee.items() if key != "_id"})

    return {
        "message": "Employee updated successfully",
        "updated_employee": updated_employee
    }