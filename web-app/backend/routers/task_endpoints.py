from fastapi import APIRouter, HTTPException, Depends
from typing import Callable,List
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from task.task_handler import(
    post_new_task
)
from models import User
from auth.auth_handler import get_current_active_user
from schemas import TaskCreate,TaskResponse
from database import get_db

router = APIRouter()

async def handle_request(func: Callable, *args, **kwargs):
    """Encapsula chamadas para tratamento padronizado de erros"""
    try:
        if asyncio.iscoroutinefunction(func):  # Verifica se a função é async
            return await func(*args, **kwargs)
        return func(*args, **kwargs)  # Executa normalmente se for síncrona 
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/lab/{lab_id}")
async def get_task_for_lab():
    pass

@router.get("/machine/{machine_key}")
async def get_task_for_lab():
    pass

@router.post("/new")
async def new_task_endpoint(new_task:TaskCreate,user: User = Depends(get_current_active_user),db: AsyncSession = Depends(get_db)):
    return await handle_request(
        post_new_task,
        new_task=new_task,
        user=user,
        db=db
    )

@router.post("/complete/{task_id}")
async def complete_task_endpoint():
    pass

@router.patch("/update/{task_id}")
async def update_task_endpoint():
    pass

