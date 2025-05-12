from fastapi import APIRouter, HTTPException, Depends
from typing import Callable,List
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from session.session_handler import (
    post_new_session,get_sessions_for_lab,get_sessions_for_machine,get_sessions_for_student
)
from database import get_db
from schemas import SessionCreate,SessionResponse


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
    

@router.post("/new/{machine_key}")
async def new_session_endpoint(machine_key: str, new_session: SessionCreate, db: AsyncSession = Depends(get_db)):
    return await handle_request(
        post_new_session,  # objeto do schema com os dados da requisição
        machine_key=machine_key,
        session=new_session,
        db=db
    )

@router.get("/lab/{lab_id}", response_model=List[SessionResponse])
async def get_sessions_for_lab_endpoint(lab_id: str, db: AsyncSession = Depends(get_db)):
    return await handle_request(
        get_sessions_for_lab,
        lab_id=lab_id,
        db=db
    )

@router.get("/machine/{machine_key}", response_model=List[SessionResponse])
async def get_sessions_for_machine_endpoint(machine_key: str, db: AsyncSession = Depends(get_db)):
    return await handle_request(
        get_sessions_for_machine,
        machine_key=machine_key,
        db=db
    )

@router.get("/student/{student_id}", response_model=List[SessionResponse])
async def get_sessions_for_endpoint_student(student_id: str, db: AsyncSession = Depends(get_db)):
    return await handle_request(
        get_sessions_for_student,
        student_id=student_id,
        db=db
    )



