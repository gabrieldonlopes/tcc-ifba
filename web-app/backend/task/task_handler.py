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

#TODO: dividir essa função em pequenas tarefas
async def post_new_task(new_task: TaskCreate, user:User,db:AsyncSession):
    # verifica se task já existe
    task_result = await db.execute(select(Task).where(func.lower(Task.task_name) == new_task.task_name.lower()))
    task_obj = task_result.scalars().first()

    if task_obj:
        raise HTTPException(status_code=409, detail="Tarefa criada já existe")
    
    lab_result = await db.execute(select(Lab).where(Lab.lab_id == new_task.lab_id).options(
                selectinload(Lab.users),
                selectinload(Lab.machines)
            ))
    lab_obj = lab_result.scalars().first()

    # verifica existência do lab
    if not lab_obj:
        raise HTTPException(status_code=404,detail="Lab não foi encontrado")
    if not any(u.user_id == user.user_id for u in lab_obj.users): # verificação se user pode criar um task no lab
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operação não autorizada")

    # transforma as máquinas em obj e verifica se existem e estão no lab
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
    
async def get_tasks_for_lab(lab_id:str,user:User,db:AsyncSession) -> List[TaskResponse]:
    lab_result = await db.execute(select(Lab).where(Lab.lab_id == lab_id)
                                  .options(selectinload(Lab.users),selectinload(Lab.tasks).selectinload(Task.machines)))
    lab_obj = lab_result.scalars().first()
    
    # verifica existência do lab
    if not lab_obj:
        raise HTTPException(status_code=404,detail="Lab não foi encontrado")
    if not any(u.user_id == user.user_id for u in lab_obj.users): # verificação se user pode criar um task no lab
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operação não autorizada")


    return [
        TaskResponse(
            task_id=t.task_id,
            task_name=t.task_name,
            task_description=t.task_description,
            is_complete=t.is_complete,
            task_creation=t.task_creation.isoformat(),
            machine_keys=[m.machine_key for m in t.machines],
            machine_names=[m.machine_name for m in t.machines]
        )
        for t in lab_obj.tasks
    ]

async def get_tasks_for_machine(machine_key: str, user: User, db: AsyncSession) -> List[TaskResponse]:
    result = await db.execute(
        select(Machine)
        .where(Machine.machine_key == machine_key)
        .options(
            selectinload(Machine.lab).selectinload(Lab.users),  # carrega os usuários do lab
            selectinload(Machine.tasks).selectinload(Task.machines)  # carrega as tasks da máquina
        )
    )
    machine_obj = result.scalars().first()

    if not machine_obj:
        raise HTTPException(status_code=404, detail="Máquina não foi encontrada")

    # Verifica se o usuário está associado ao laboratório da máquina
    if not any(u.user_id == user.user_id for u in machine_obj.lab.users):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operação não autorizada")

    return [
        TaskResponse(
            task_id=t.task_id,
            task_name=t.task_name,
            task_description=t.task_description,
            is_complete=t.is_complete,
            task_creation=t.task_creation.isoformat(),
            machine_keys=[m.machine_key for m in t.machines],
            machine_names=[m.machine_name for m in t.machines]
        )
        for t in machine_obj.tasks
    ]

async def complete_task(task_id:int,user:User,db:AsyncSession):
    task_result = await db.execute(
        select(Task)
        .where(Task.task_id == task_id)
        .options(selectinload(Task.user))
    )
    task_obj = task_result.scalars().first()

    if not task_obj:
        raise HTTPException(status_code=404,detail="Tarefa não foi encontrada")
    if not (task_obj.user.user_id == user.user_id): # verificação se user pode criar um task no lab
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operação não autorizada")
    if task_obj.is_complete:
        raise HTTPException(status_code=409,detail="A tarefa já foi concluída anteriormente")
    
    task_obj.is_complete = True
    try: 
        await db.commit()
        await db.refresh(task_obj)

        return {"message":"Tarefa concluída com sucesso!"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

