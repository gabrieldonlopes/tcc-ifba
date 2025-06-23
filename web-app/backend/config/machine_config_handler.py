import asyncio
from datetime import datetime
from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select
from sqlalchemy import or_
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from models import User
from schemas import MachineConfig,NewMachineConfig,MachineNewState,MachineNewCheck
from models import Machine, Lab, StateCleanliness
from config.lab_handler import verify_lab

async def get_machine_config(machine_key:str, db: AsyncSession) -> MachineConfig:
    result = await db.execute(select(Machine).filter(Machine.machine_key == machine_key))
    machine_config_obj = result.scalars().first()

    if not machine_config_obj:
        raise HTTPException(status_code=404,detail="Computador não foi encontrado")

    return MachineConfig(
        motherboard=machine_config_obj.motherboard,
        machine_name=machine_config_obj.machine_name,
        memory=machine_config_obj.memory,
        storage=machine_config_obj.storage,
        state_cleanliness=machine_config_obj.state_cleanliness,
        last_checked=machine_config_obj.last_checked.strftime("%d/%m/%Y"),
        lab_id=machine_config_obj.lab_id
    )

async def verify_user_for_machine(machine_key:str,user:User,db: AsyncSession) -> Machine:
    result = await db.execute(select(Machine)
            .where(Machine.machine_key == machine_key
        ).options(
            selectinload(Machine.lab).selectinload(Lab.users)
        )
    )
    machine_obj = result.scalars().first()

    if not machine_obj:
        raise HTTPException(status_code=404,detail="Computador não foi encontrado")

    if user not in machine_obj.lab.users:
        raise HTTPException(status_code=403,detail="Usuário não autorizado")
    
    return machine_obj

async def post_new_machine_config(new_machine:NewMachineConfig, db: AsyncSession):
    if not await verify_lab(new_machine.lab_id,db=db):
        raise HTTPException(status_code=404,detail="Lab não foi encontrado")

    existing_machine = await db.execute(
        select(Machine).where(or_(
            Machine.machine_key == new_machine.machine_key,
            Machine.machine_name == new_machine.machine_name
        ))    
    )
    new_machine.last_checked = datetime.strptime(new_machine.last_checked, "%d/%m/%Y")
    if existing_machine.scalars().first():
        raise HTTPException(status_code=400,detail="Computador já registrado")
        
    db_machine = Machine(
        machine_name=new_machine.machine_name,
        motherboard=new_machine.motherboard,
        memory=new_machine.memory,
        storage=new_machine.storage,
        state_cleanliness=new_machine.state_cleanliness,
        last_checked=new_machine.last_checked,
        lab_id=new_machine.lab_id,
        machine_key=new_machine.machine_key
    )
    
    try:
        db.add(db_machine)
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar computador. Detalhes: {str(e)}",
        )
    return {"message":"Configuração do computador registrada com Sucesso!"}

async def delete_machine(machine_key:str, user:User,db:AsyncSession):
    machine_config_obj = await verify_user_for_machine(machine_key=machine_key,user=user,db=db)

    await db.delete(machine_config_obj)
    await db.commit()
    
    return {"message":"Computador removido do Laboratório com Sucesso"}

async def update_last_check(machine_key:str,new_check:MachineNewCheck,user:User,db:AsyncSession):
    machine_obj = await verify_user_for_machine(machine_key=machine_key,user=user,db=db)

    try:
        try:
            for_new_check = datetime.strptime(new_check.new_check, "%d/%m/%Y")
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail="Formato de data incorreto"
            )
        machine_obj.last_checked = for_new_check
        await db.commit()
        await db.refresh(machine_obj)
        
        return {"message": "Última checagem atualizada"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

async def update_state_cleanliness(machine_key:str,new_state:MachineNewState,user:User,db:AsyncSession):
    machine_obj = await verify_user_for_machine(machine_key=machine_key,user=user,db=db)

    try:
        try:
            state_enum_value = StateCleanliness(new_state.new_state.upper())
        except ValueError:
            valid_states = ", ".join([s.value for s in StateCleanliness])
            raise HTTPException(
                status_code=422, # Unprocessable Entity (more specific than 400 for invalid value for a field)
                detail=f"Valor inválido para o estado de limpeza: '{new_state}'. Valores permitidos: {valid_states}."
            )

        machine_obj.state_cleanliness = state_enum_value
        
        await db.commit()
        await db.refresh(machine_obj)
        
        return {"message": "Estado de limpeza da máquina atualizado com sucesso"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

#TODO: esse método deve ser restrito
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
        new_config.last_checked = datetime.strptime(new_config.last_checked, "%d/%m/%Y")
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
