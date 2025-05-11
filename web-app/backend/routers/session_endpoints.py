from fastapi import APIRouter, HTTPException, Depends
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from session.session_handler import post_new_session

from database import get_db
from schemas import SessionCreate


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