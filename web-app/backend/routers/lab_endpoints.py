import asyncio

from fastapi import APIRouter, HTTPException, Depends
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession 
from database import get_db
from typing import List

from schemas import LabCreate,LabResponse,LabUpdate,MachineConfigResponse,UserResponse,StudentResponse
from models import User
from auth.auth_handler import get_current_active_user
from config.lab_handler import (
    get_lab, create_lab, update_lab, delete_lab,join_lab,get_machines_for_lab,
    get_users_for_lab,get_students_for_lab
)
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
    

@router.get("/{lab_id}", response_model=LabResponse)
async def get_lab_endpoint(lab_id: str, db: AsyncSession = Depends(get_db)):
    return await handle_request(get_lab, lab_id=lab_id, db=db)

@router.post("/new_lab")
async def create_lab_endpoint(new_lab: LabCreate,user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    return await handle_request(create_lab,user=user, new_lab=new_lab, db=db)

@router.patch("/update/{lab_id}")
async def update_lab_endpoint(lab_id: str, new_lab: LabUpdate,user: User = Depends(get_current_active_user),db: AsyncSession = Depends(get_db)):
    return await handle_request(update_lab, lab_id=lab_id, new_lab=new_lab, user=user,db=db)

@router.post("/join/{lab_id}")
async def join_lab_endpoint(lab_id:str,user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    return await handle_request(join_lab,lab_id=lab_id,user=user,db=db)

@router.delete("/delete/{lab_id}")
async def delete_lab_endpoint(lab_id: str,user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    return await handle_request(delete_lab, lab_id=lab_id, db=db,user=user)

# esse métodos podem ser utilizados pelo desktop-app, por isso não precisam de user
@router.get("/{lab_id}/machines", response_model=List[MachineConfigResponse])
async def get_machines_for_lab_endpoint(lab_id:str,db: AsyncSession = Depends(get_db)):
    return await handle_request(get_machines_for_lab,lab_id=lab_id,db=db)

@router.get("/{lab_id}/students", response_model=List[StudentResponse])
async def get_students_for_lab_endpoints(lab_id:str,db: AsyncSession = Depends(get_db)):
    return await handle_request(get_students_for_lab,lab_id=lab_id,db=db)

@router.get("/{lab_id}/users", response_model=List[UserResponse])
async def get_users_for_lab_endpoint(lab_id:str,db: AsyncSession = Depends(get_db)):
    return await handle_request(get_users_for_lab,lab_id=lab_id,db=db)  