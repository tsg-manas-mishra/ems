from fastapi import HTTPException, Query
from typing import Optional
from db import user_collection

def get_all_users_service(column: Optional[str] = None, order: Optional[str] = "asc"):
    """
    Fetch all users with optional sorting.
    """
    try:
        allowed_columns = ["name", "email", "role", "department", "designation", "address", "contact"]

        if column and column not in allowed_columns:
            raise HTTPException(status_code=400, detail=f"Invalid column '{column}'. Allowed: {allowed_columns}")

        sort_order = 1 if order == "asc" else -1  # 1 = ascending, -1 = descending

        query = {}  # Fetch all users
        users = list(user_collection.find(query, {"password": 0}))

        if column:
            users.sort(key=lambda x: x.get(column, ""), reverse=(order == "desc"))

        for user in users:
            user["_id"] = str(user["_id"])  # Convert ObjectId to string

        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
