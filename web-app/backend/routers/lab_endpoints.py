import asyncio

from fastapi import APIRouter, HTTPException, Depends
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession 
from database import get_db

from schemas import LabCreate,LabResponse,LabUpdate
from config.lab_handler import get_lab, create_lab, update_lab, delete_lab

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
async def create_lab_endpoint(new_lab: LabCreate, db: AsyncSession = Depends(get_db)):
    return await handle_request(create_lab, new_lab=new_lab, db=db)

@router.patch("/update/{lab_id}")
async def update_lab_endpoint(lab_id: str, new_lab: LabUpdate, db: AsyncSession = Depends(get_db)):
    return await handle_request(update_lab, lab_id=lab_id, new_lab=new_lab, db=db)

@router.delete("/delete/{lab_id}")
async def delete_lab_endpoint(lab_id: str, db: AsyncSession = Depends(get_db)):
    return await handle_request(delete_lab, lab_id=lab_id, db=db)
