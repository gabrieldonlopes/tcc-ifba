from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlalchemy import func
from typing import List
from datetime import datetime

from models import User,Machine,Task,Lab
from schemas import TaskCreate,TaskResponse

async def post_new_task(new_task: TaskCreate, user:User,db:AsyncSession):
    # verifica se task já existe
    task_result = await db.execute(select(Task).where(func.lower(Task.task_name) == new_task.task_name.lower()))
    task_obj = task_result.scalars().first()

    if task_obj: # essa é realmente a exceção correta?
        raise HTTPException(status_code=409, detail="Tarefa criada já existe")
    
    lab_result = await db.execute(select(Lab).where(Lab.lab_id == new_task.lab_id).options(
                selectinload(Lab.users),
                selectinload(Lab.machines)
            ))
    lab_obj = lab_result.scalars().first()

    if not lab_obj:
            raise HTTPException(status_code=404,detail="Lab não foi encontrado")
    if not any(u.user_id == user.user_id for u in lab_obj.users):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operação não autorizada")

    machine_keys = new_task.machines

    machines_result = await db.execute( # busca todas as machines que correspondem as keys passadas
        select(Machine).where(
            Machine.machine_key.in_(machine_keys), # o operador IN é de suma importância aqui
            Machine.lab_id == new_task.lab_id
        )
    )
    # antiga função fazia uma query para cada key, essa é muito mais eficiente
    machines_obj = machines_result.scalars().all() # adiciona as achadas no obj

    if len(machines_obj) != len(machine_keys): # caso o tamanho seja diferente, alguma máquina não existe
        raise HTTPException(
            status_code=404,
            detail="Uma ou mais máquinas não foram encontradas ou não pertencem ao laboratório"
        )

    db_task = Task(
        task_name=new_task.task_name,
        task_description=new_task.task_description,
        task_creation=datetime.now(),
        lab_id=new_task.lab_id,
        user_id=user.user_id,
        machines=machines_obj
    )

    try:
        db.add(db_task)
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar tarefa. Detalhes: {str(e)}",
        )
    return {"message":"Tarefa registrada com Sucesso!"}
    
