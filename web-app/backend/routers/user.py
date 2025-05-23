from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from auth.auth_handler import get_current_active_user, get_user_by_id
from schemas import UserResponse,LabResponseUser
from config.lab_handler import get_lab_for_user
from models import User
from database import get_db

router = APIRouter()

@router.get("/users/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_user_by_id(db, user_id)

@router.get("/users/me/labs", response_model=List[LabResponseUser])
async def get_current_user_labs(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    return await get_lab_for_user(user=user, db=db)