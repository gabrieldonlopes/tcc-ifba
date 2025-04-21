import asyncio
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select
from sqlalchemy import or_

from schemas import MachineConfig,NewMachineConfig
from models import Machine, Lab

async def verify_lab(lab_id: str, db: AsyncSession) -> bool:
    lab_obj = await db.execute(select(Lab).filter(Lab.lab_id == lab_id))
    existing_lab = lab_obj.scalars().first()
    return True if existing_lab else False

async def get_machine_config(machine_key:str, db: AsyncSession) -> MachineConfig:
    result = await db.execute(select(Machine).filter(Machine.machine_key == machine_key))
    machine_config_obj = result.scalars().first()

    if not machine_config_obj:
        raise HTTPException(status_code=404,detail="Computador não foi encontrado")

    return MachineConfig(
        motherboard=machine_config_obj.motherboard,
        name=machine_config_obj.name,
        memory=machine_config_obj.memory,
        storage=machine_config_obj.storage,
        state_cleanliness=machine_config_obj.state_cleanliness,
        last_checked=machine_config_obj.last_checked.strftime("%d-%m-%Y"),
        lab_id=machine_config_obj.lab_id
    )

async def post_new_machine_config(new_machine:NewMachineConfig, db: AsyncSession):
    if not await verify_lab(new_machine.lab_id,db=db):
        raise HTTPException(status_code=404,detail="Lab não foi encontrado")

    existing_machine = await db.execute(
        select(Machine).where(or_(
            Machine.machine_key == new_machine.machine_key,
            Machine.name == new_machine.name
        ))    
    )
    new_machine.last_checked = datetime.strptime(new_machine.last_checked, "%d-%m-%Y")
    if existing_machine.scalars().first() == None:
        db_machine = Machine(
            name=new_machine.name,
            motherboard=new_machine.motherboard,
            memory=new_machine.memory,
            storage=new_machine.storage,
            state_cleanliness=new_machine.state_cleanliness,
            last_checked=new_machine.last_checked,
            lab_id=new_machine.lab_id,
            machine_key=new_machine.machine_key
        )
        db.add(db_machine)
        await db.commit()
        return {"message":"Configuração do computador registrada com Sucesso!"}
    else:
        raise HTTPException(status_code=400,detail="Computador já registrado")

async def delete_machine(machine_key:str, db:AsyncSession):
    result = await db.execute(select(Machine).filter(Machine.machine_key == machine_key))
    machine_config_obj = result.scalars().first()
    
    if not machine_config_obj:
        raise HTTPException(status_code=404,detail="Computador não foi encontrado") 
    
    await db.delete(machine_config_obj)
    await db.commit()
    
    return {"message":"Computador removido do Laboratório com Sucesso"}

async def update_machine_config(machine_key:str,new_config:MachineConfig, db:AsyncSession):
    if not await verify_lab(new_config.lab_id,db=db):
        raise HTTPException(status_code=404,detail="Lab não foi encontrado")
    try:
        result = await db.execute(select(Machine).filter(Machine.machine_key == machine_key))
        machine_config_obj = result.scalars().first()

        if not machine_config_obj:
            raise HTTPException(status_code=404,detail="Computador não foi encontrado")

        # utilizar getters e setters dinamicamente para alterar apenas se o valor não for
        # vazio e se ele for diferente do que o já armazenado na db 
        new_config.last_checked = datetime.strptime(new_config.last_checked, "%d-%m-%Y")
        for field, new_value in new_config.dict().items():
            if new_value is not None:
                current_value = getattr(machine_config_obj, field, None)
                if new_value != current_value:
                    setattr(machine_config_obj, field, new_value)
                    
        await db.commit()
        await db.refresh(machine_config_obj)

        return {"message": "Configuração da máquina salva com sucesso"}
    
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))