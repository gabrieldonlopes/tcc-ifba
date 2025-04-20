import asyncio

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select

from schemas import MachineConfig,NewMachineConfig
from models import Machine


async def get_machine_config(machine_key:str, db: AsyncSession) -> MachineConfig:
    result = await db.execute(select(Machine).filter(Machine.machine_key == machine_key))
    machine_config_obj = result.scalars().first()

    if not machine_config_obj:
        raise HTTPException(status_code=404,detail="Machine not Found")

    return MachineConfig(
        motherboard=machine_config_obj.motherboard,
        name=machine_config_obj.name,
        memory=machine_config_obj.memory,
        storage=machine_config_obj.storage,
        state_cleanliness=machine_config_obj.state_cleanliness,
        last_checked=machine_config_obj.last_checked,
        lab_id=machine_config_obj.lab_id
    )

async def post_new_machine_config(new_machine:NewMachineConfig, db: AsyncSession):
    existing_machine = await db.execute(
        select(Machine).where(
            Machine.machine_key == new_machine.machine_key,
            Machine.name == new_machine.name
        )    
    )
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
        return {"message":"Machine Config registered successfully"}
    else:
        raise HTTPException(status_code=400,detail="Machine already registered.")

async def delete_machine(machine_key:str, db:AsyncSession):
    result = await db.execute(select(Machine).filter(Machine.machine_key == machine_key))
    machine_config_obj = result.scalars().first()
    
    if not machine_config_obj:
        raise HTTPException(status_code=404,detail="Machine not Found") 
    
    await db.delete(machine_config_obj)
    await db.commit()
    
    return {"message":"Machine deleted from Lab successfully"}

async def update_machine_config(machine_key:str,new_config:MachineConfig, db:AsyncSession):
    try:
        result = await db.execute(select(Machine).filter(Machine.machine_key == machine_key))
        machine_config_obj = result.scalars().first()

        if not machine_config_obj:
            raise HTTPException(status_code=404,detail="Machine not Found")

        # utilizar getters e setters dinamicamente para alterar apenas se o valor não for
        # vazio e se ele for diferente do que o já armazenado na db 
        for field, new_value in new_config.dict().items():
            if new_value is not None:
                current_value = getattr(machine_config_obj, field, None)
                if new_value != current_value:
                    setattr(machine_config_obj, field, new_value)
                    
        await db.commit()
        await db.refresh(machine_config_obj)

        return {"message": "Machine config updated successfully"}
    
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))