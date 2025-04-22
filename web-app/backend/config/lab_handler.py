from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession 

from schemas import LabCreate,LabResponse
from models import Lab

async def get_lab(lab_id:str, db: AsyncSession) -> LabResponse:
    pass

async def create_lab(new_lab: LabCreate, db: AsyncSession):
    pass

async def update_lab(lab_id: str, new_lab: LabCreate, db: AsyncSession):
    pass

async def delete_lab(lab_id: str, db: AsyncSession):
    pass