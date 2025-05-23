from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from typing import List
from schemas import (
    LabCreate,LabResponse,LabResponseUser,LabUpdate,MachineConfigResponse,UserResponse
)
from models import Lab,User

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

#TODO: adicionar tratamento de erro mais especifíco
async def create_lab(new_lab: LabCreate,user:User, db: AsyncSession):
    lab_obj = await verify_lab(lab_id=new_lab.lab_id,db=db)
    if lab_obj:
        raise HTTPException(status_code=400,detail="Lab já registrado")
    
    db_lab = Lab(
        lab_id=new_lab.lab_id,
        lab_name=new_lab.lab_name,
        classes=new_lab.classes
    ) 
     # Associa o usuário ao lab
    db_lab.users.append(user)
    
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

async def get_machines_for_lab(lab_id:str,db:AsyncSession) -> List[MachineConfigResponse]:
    result = await db.execute(
        select(Lab).where(Lab.lab_id==lab_id).options(
            selectinload(Lab.machines)
        )
    )
    lab = result.scalars().first()
    if not lab:
        raise HTTPException(status_code=404, detail="Lab não foi encontrado")
    if lab.machines==None:
        raise HTTPException(status_code=404, detail="Nenhuma máquina foi encontrada")

    return [
        MachineConfigResponse(
            machine_key=m.machine_key,
            machine_name=m.machine_name,
            state_cleanliness=m.state_cleanliness,
            last_checked=m.last_checked.strftime("%d/%m/%Y"),
        )
        for m in lab.machines
    ]

async def get_lab_for_user(user:User,db:AsyncSession) -> List[LabResponseUser]:
    result = await db.execute(
        select(User).where(User.user_id==user.user_id).options(
            selectinload(User.labs)
        )
    )
    user_obj = result.scalars().first()
    
    print(user_obj.username)
    if not user_obj:
        raise HTTPException(status_code=404,detail="Usuário não foi encontrado")
    elif user_obj.labs == None:
        raise HTTPException(status_code=404,detail="Nenhum laboratório foi encontrado")
    
    return [ 
        LabResponseUser(
            lab_id=l.lab_id,
            lab_name=l.lab_name,
            classes=l.classes.split(",")
        )
        for l in user_obj.labs
    ]

async def get_users_for_lab(lab_id:str,db:AsyncSession) -> List[UserResponse]:
    result = await db.execute(
        select(Lab).where(Lab.lab_id==lab_id).options(
            selectinload(Lab.users)
        )
    )
    lab = result.scalars().first()
    
    if not lab:
        raise HTTPException(status_code=404, detail="Lab não foi encontrado")
    if lab.users==None: # isso aqui é impossível de acontecer
        raise HTTPException(status_code=404, detail="Nenhuma Usuário foi encontrado")

    return [
        UserResponse(
            user_id=u.user_id,
            username=u.username,
            email=u.email
        )
        for u in lab.users
    ]
