from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import or_,func

from typing import List
from schemas import (
    LabCreate,LabResponse,LabResponseUser,LabUpdate,
    MachineConfigResponse,UserResponse,StudentResponse,
    LastSessionResponse
)
from models import Lab,User,Machine,Student,Session,user_lab_association,Task

async def verify_lab(lab_id: str, db: AsyncSession,user:User=None) -> Lab:
    if user is not None:
        lab_obj = await db.execute(
            select(Lab).where(Lab.lab_id == lab_id).options(
                selectinload(Lab.users)
            ))
        existing_lab = lab_obj.scalars().first()
        if not existing_lab:
            raise HTTPException(status_code=404,detail="Lab não foi encontrado")
        if not any(u.user_id == user.user_id for u in lab_obj.users):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operação não autorizada")
    lab_obj = await db.execute(select(Lab).where(Lab.lab_id == lab_id))
    existing_lab = lab_obj.scalars().first()
    if not existing_lab:
        raise HTTPException(status_code=404,detail="Lab não foi encontrado")

    return existing_lab

async def get_lab(lab_id: str, db: AsyncSession) -> LabResponse:
    lab_obj = await verify_lab(lab_id=lab_id, db=db)

    # Contagens restritas ao lab
    machine_count_query = select(func.count(Machine.machine_key)).where(Machine.lab_id == lab_id)
    student_count_query = select(func.count(Student.student_id)).join(Session).where(Session.lab_id == lab_id)
    users_count_query = select(func.count(user_lab_association.c.user_id)).where(user_lab_association.c.lab_id == lab_id)
    task_count_query = select(func.count(Task.task_id)).where(Task.lab_id == lab_id)

    machine_result = await db.execute(machine_count_query)
    student_result = await db.execute(student_count_query)
    user_result = await db.execute(users_count_query)
    task_result = await db.execute(task_count_query)

    return LabResponse(
        lab_name=lab_obj.lab_name,
        classes=lab_obj.classes.split(","),
        machine_count=machine_result.scalar_one(),
        student_count=student_result.scalar_one(),
        user_count=user_result.scalar_one(),
        task_count=task_result.scalar_one()  # novo campo
    )

async def create_lab(new_lab: LabCreate,user:User, db: AsyncSession):
    result = await db.execute(select(Lab).where(
        or_(
            Lab.lab_id == new_lab.lab_id,
            Lab.lab_name == new_lab.lab_name
    )))

    lab_obj = result.scalars().first()
    
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
    await db.refresh(db_lab)
    
    return {"message":"Lab criado com Sucesso"}

async def delete_lab(lab_id: str, db: AsyncSession,user:User):
    lab_obj = await verify_lab(lab_id=lab_id,db=db,user=user)

    await db.delete(lab_obj)
    await db.commit()

    return {"message":"Lab excluido com sucesso"}

async def update_lab(lab_id: str, new_lab: LabUpdate,user:User, db: AsyncSession):
    lab_obj = await verify_lab(lab_id=lab_id, db=db,user=user)

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

        return {"message": "Lab foi alterado com sucesso"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar Lab: {str(e)}")

async def join_lab(lab_id:str,user:User,db:AsyncSession):
    lab_obj = await db.execute(
        select(Lab).where(Lab.lab_id == lab_id).options(
            selectinload(Lab.users)
        ))
    existing_lab = lab_obj.scalars().first()
    if not existing_lab:
        raise HTTPException(status_code=404,detail="Lab não foi encontrado")
    if user in existing_lab.users:
        raise HTTPException(status_code=409,detail="Você já está neste lab")

    existing_lab.users.append(user)
    await db.commit()
    await db.refresh(existing_lab)

    return {"message": "Você entrou no lab com sucesso"}

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
            motherboard=m.motherboard,
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

async def get_students_for_lab(lab_id: str, db: AsyncSession) -> List[StudentResponse]:
    result = await db.execute(
        select(Lab)
        .where(Lab.lab_id == lab_id)
        .options(
            selectinload(Lab.sessions).selectinload(Session.student)
        )
    )
    lab = result.scalars().first()
    
    if not lab:
        raise HTTPException(status_code=404, detail="Lab não foi encontrado")

    sessions_by_student = {}
    for session in lab.sessions:
        student = session.student
        if student:
            current_latest = sessions_by_student.get(student.student_id)
            if current_latest is None or session.session_start > current_latest.session_start:
                sessions_by_student[student.student_id] = session

    response_list = []
    for student_id, last_session in sessions_by_student.items():
        student = last_session.student
        response_list.append(
            StudentResponse(
                student_id=student.student_id,
                student_name=student.student_name,
                class_var=student.class_var,
                last_session=LastSessionResponse(
                    session_id=last_session.session_id,
                    session_start=last_session.session_start,
                    lab_id=last_session.lab_id,
                    machine_key=last_session.machine_key,
                )
            )
        )

    return response_list