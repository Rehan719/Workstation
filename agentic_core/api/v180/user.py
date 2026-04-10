from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

router = APIRouter(prefix="/user", tags=["User & RBAC"])

# Mock User database
USERS = {
    "demo_user": {
        "id": "demo_user",
        "name": "Abdullah",
        "email": "abdullah@workstation.ai",
        "role": "admin",
        "persona": "Sovereign Citizen"
    }
}

@router.get("/profile/{user_id}")
async def get_profile(user_id: str):
    user = USERS.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/profile/{user_id}/role")
async def update_role(user_id: str, role: str):
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    if role not in ["admin", "user", "guest"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    USERS[user_id]["role"] = role
    return {"status": "success", "new_role": role}
