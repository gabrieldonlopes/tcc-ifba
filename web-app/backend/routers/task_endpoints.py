from fastapi import APIRouter, HTTPException, Depends
from typing import Callable,List
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from task.task_handler import(
    post_new_task,get_tasks_for_lab,get_tasks_for_machine
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
    

@router.get("/lab/{lab_id}",response_model=List[TaskResponse])
async def get_task_for_lab(lab_id:str,user: User = Depends(get_current_active_user),db: AsyncSession = Depends(get_db)):
    return await handle_request(
        get_tasks_for_lab,
        lab_id=lab_id,
        user=user,
        db=db
    )

@router.get("/machine/{machine_key}",response_model=List[TaskResponse])
async def get_task_for_machine(machine_key:str,user: User = Depends(get_current_active_user),db: AsyncSession = Depends(get_db)):
    return await handle_request(
        get_tasks_for_machine,
        machine_key=machine_key,
        user=user,
        db=db
    )

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

