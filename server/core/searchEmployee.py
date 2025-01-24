from fastapi import HTTPException, Query
from db import mycollection
from pydantic import EmailStr
from typing import Optional
from bson import ObjectId

def searchEmp(name: Optional[str] = Query(None), designation: Optional[str] = Query(None),department: Optional[str]=Query(None)):
    try:
        query={}
        if name:
            query["name"]=name
        if designation:
            query["designation"]=designation
        if department:
            query["department"]=department
        employees=list(mycollection.find(query))
        for emp in employees:
            emp["_id"] = str(emp["_id"])
        del emp["password"]
        return {"employees":employees}
    except Exception as e:
        raise HTTPException("")
    