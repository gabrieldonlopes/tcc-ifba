import asyncio

from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession 

from models import User
from auth.auth_handler import get_current_active_user
from database import get_db
from schemas import MachineConfig, NewMachineConfig,MachineNewCheck,MachineNewState
from config.machine_config_handler import (
    get_machine_config,post_new_machine_config,
    delete_machine, update_machine_config,
    update_last_check,update_state_cleanliness
)

router = APIRouter()

# TODO: verificar necessidade de fazer uma verificacao de lab_id

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

@router.get("/{machine_key}", response_model=MachineConfig)
async def get_machine_config_endpoint(machine_key: str, db: AsyncSession = Depends(get_db)):
    return await handle_request(get_machine_config, machine_key=machine_key, db=db)

@router.post("/new_machine")
async def post_machine_config_endpoint(new_machine: NewMachineConfig, db: AsyncSession = Depends(get_db)):
    return await handle_request(post_new_machine_config, new_machine=new_machine, db=db)

@router.delete("/delete/{machine_key}")
async def delete_machine_endpoint(machine_key: str,user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    return await handle_request(delete_machine, machine_key=machine_key,user=user, db=db)

@router.patch("/update/{machine_key}/last_check")
async def update_machine_last_check_endpoint(machine_key: str,new_check:MachineNewCheck, user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    return await handle_request(update_last_check,machine_key=machine_key,new_check=new_check,user=user,db=db)

@router.patch("/update/{machine_key}/state_cleanliness")
async def update_machine_state_cleanliness_endpoint(machine_key: str,new_state:MachineNewState, user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    return await handle_request(update_state_cleanliness,machine_key=machine_key,new_state=new_state,user=user,db=db)

# endpoint restrito a desktop-app
@router.patch("/update/{machine_key}")
async def update_machine_config_endpoint(machine_key: str, new_config: MachineConfig, db: AsyncSession = Depends(get_db)):
    return await handle_request(update_machine_config, machine_key=machine_key, new_config=new_config, db=db)