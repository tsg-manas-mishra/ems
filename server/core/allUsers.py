from fastapi import HTTPException
from fastapi.responses import JSONResponse
from db import user_collection

def getusers(payload: dict):
    role = payload.get("role")
    try:
        if not role:
            return JSONResponse(status_code=401, content={"message": "Role missing"})

        if role in ["Admin", "Employee"]:
            users = list(user_collection.find())
            for user in users:
                user["_id"] = str(user["_id"])  # Ensure _id is serializable
            return users
        else:
            raise JSONResponse(status_code=403, content="Forbidden Access")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch users: {str(e)}")

