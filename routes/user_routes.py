from fastapi import APIRouter, HTTPException, Depends

from auth.auth import get_current_user
from database.database import get_user, patch_user

user_router = APIRouter()


@user_router.get("/users/{user_id}")
async def get_user_endpoint(user_id: int, current_user: dict = Depends(get_current_user)):
    user = await get_user(user_id)
    print(current_user)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.get("/me")
async def get_current_user(current_user: dict = Depends(get_current_user)):

    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return current_user


@user_router.patch("/users/{user_id}")
async def patch_user_data(user_id: int, user_registered: dict, current_user: dict = Depends(get_current_user)):
    user_mod = await patch_user(user_id, user_registered)
    if user_mod is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_mod = await get_user(user_id)
    return user_mod
