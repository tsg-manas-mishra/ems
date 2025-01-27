from fastapi import HTTPException, Depends
from utils import decode_token

def admin_dashboard(payload: dict = Depends(decode_token)):
    """
    to redirect the user to admin dashboard based on the role in token
    """
    role = payload["role"]
    #if payload in empty or the rol field does not exist
    if payload is None:
        raise HTTPException(status_code=400,detail="Payload empty")
    #if payload has a role which is not Admin
    if role is None or role!="Admin":
        raise HTTPException(status_code=403,detail="Forbidden Access")
    try:
        return {"message":"Welcome to Admin Dashboard"}
    except:
        raise HTTPException(status_code=500,detail="Internal Server Error")