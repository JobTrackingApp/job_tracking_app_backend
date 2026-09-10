from fastapi import Header, HTTPException
from firebase_admin import auth
from fastapi import Depends
from app.core.database import users_collection

# Verify Firebase ID token
async def get_current_user(authorization: str = Header(...)):

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header"
        )

    token = authorization.split(" ", 1)[1]

    try:
        decoded_token = auth.verify_id_token(token)

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return decoded_token

# Get corresponding user from MongoDB
async def get_current_db_user(
    firebase_user = Depends(get_current_user)
):

    firebase_uid = firebase_user["uid"]

    user = await users_collection.find_one(
        {
            "firebase_uid": firebase_uid,
            "is_active": True
        },
        {
            "_id": 0
        }
    )

    if not user:
        raise HTTPException(
            status_code=403,
            detail="User account is not registered or inactive"
        )

    return user

# Role-based authorization
def require_roles(*allowed_roles):

    async def role_checker(
        current_user = Depends(get_current_db_user)
    ):

        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions"
            )

        return current_user

    return role_checker