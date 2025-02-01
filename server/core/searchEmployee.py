from fastapi import HTTPException, Query
from db import user_collection
from fastapi.responses import JSONResponse
from typing import Optional

# key: column_name, value : column_value

def searchEmp(name: Optional[str] = Query(None), designation: Optional[str] = Query(None), department: Optional[str] = Query(None)):
    try:
        query = {}

        if name:
            query["name"] = {"$regex": name, "$options": "i"} 
        if designation:
            query["designation"] = {"$regex": designation, "$options": "i"}
        if department:
            query["department"] = {"$regex": department, "$options": "i"}

        employees = list(user_collection.find(query, {"password": 0}))

        if not employees:
            raise JSONResponse(status_code=404, content="No employees found.")

        for emp in employees:
            emp["_id"] = str(emp["_id"])

        return {"employees": employees}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
