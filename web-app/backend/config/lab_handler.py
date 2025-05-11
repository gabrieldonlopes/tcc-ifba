from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select

from schemas import LabCreate,LabResponse,LabUpdate
from models import Lab

async def verify_lab(lab_id: str, db: AsyncSession) -> Lab:
    lab_obj = await db.execute(select(Lab).filter(Lab.lab_id == lab_id))
    existing_lab = lab_obj.scalars().first()
    return existing_lab

async def get_lab(lab_id:str, db: AsyncSession) -> LabResponse:
    lab_obj = await verify_lab(lab_id=lab_id,db=db)
    if not lab_obj:
        raise HTTPException(status_code=404,detail="Lab não foi encontrado")
    
    return LabResponse(
        lab_name=lab_obj.lab_name,
        classes=lab_obj.classes.split(",")
    )

async def create_lab(new_lab: LabCreate, db: AsyncSession):
    lab_obj = await verify_lab(lab_id=new_lab.lab_id,db=db)
    if lab_obj:
        raise HTTPException(status_code=400,detail="Lab já registrado")
    
    db_lab = Lab(
        lab_id=new_lab.lab_id,
        lab_name=new_lab.lab_name,
        classes=new_lab.classes
    ) 
    db.add(db_lab)
    await db.commit()
    return {"message":"Lab criado com Sucesso"}

async def delete_lab(lab_id: str, db: AsyncSession):
    result = await db.execute(select(Lab).filter(Lab.lab_id == lab_id))
    lab_obj = result.scalars().first()

    if not lab_obj:
        raise HTTPException(status_code=404,detail="Lab não foi encontrado")

    await db.delete(lab_obj)
    await db.commit()

    return {"message":"Lab excluido com sucesso"}

async def update_lab(lab_id: str, new_lab: LabUpdate, db: AsyncSession):
    lab_obj = await verify_lab(lab_id=lab_id, db=db)
    if not lab_obj:
        raise HTTPException(status_code=404, detail="Lab não foi encontrado")
    
    try: 
        updated = False  # Flag para verificar se algo foi atualizado

        for field, new_value in new_lab.dict(exclude_unset=True).items():
            current_value = getattr(lab_obj, field, None)
            if new_value and new_value != current_value:
                setattr(lab_obj, field, new_value)
                updated = True
        
        if updated:
            await db.commit()
            await db.refresh(lab_obj)
        else:
            return {"message": "Nenhum campo foi alterado."}

        return {"message": "Lab foi alterado com sucesso", "lab": lab_obj}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar Lab: {str(e)}")
