from fastapi import HTTPException, Query
from db import user_collection
from pydantic import EmailStr
from typing import Optional
from bson import ObjectId

def searchEmp(email: Optional[str] = Query(None), designation: Optional[str] = Query(None),department: Optional[str]=Query(None)):
    try:
        query={}
        if email:
            query["email"]=email
        if designation:
            query["designation"]=designation
        if department:
            query["department"]=department
        employees=list(user_collection.find(query))
        if not employees:
            return {"message": "No employees found for the given criteria."}
        for emp in employees:
            emp["_id"] = str(emp["_id"])
        del emp["password"]
        return {"employees":employees}
    except Exception as e:
        raise HTTPException("")
    