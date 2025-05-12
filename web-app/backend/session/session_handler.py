from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from typing import List

from models import Machine, Session
from schemas import SessionCreate,SessionResponse,StudentResponse  # <- modelo Pydantic para entrada de dados
from student.student_handler import verify_student

async def post_new_session(machine_key: str, session: SessionCreate, db: AsyncSession):
    # Verifica se a máquina existe
    machine_result = await db.execute(select(Machine).filter(Machine.machine_key == machine_key))
    machine_config_obj = machine_result.scalars().first()

    # para debug
    #for name, field in session.model_dump().items():
    #    print(f"{name}: {field}")

    if not machine_config_obj:
        raise HTTPException(status_code=404, detail="Computador não foi encontrado.")
    
    # Nome do estudante convertido para minúsculas
    student_name = session.student_name.lower()

    # Verifica se o estudante existe ou registra um novo
    student_obj = await verify_student(
        student_name=student_name,
        password=session.password,
        class_var=session.class_var,
        db=db
    )

    db_session = Session(
        session_start=session.session_start,
        machine_key=machine_key,
        student_id=student_obj.student_id,
        lab_id=machine_config_obj.lab_id
    )
    
    try:
        db.add(db_session)
        await db.commit()
        await db.refresh(db_session)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao criar sessão. Tente novamente.",
        )

    return {"message":"Sessao registrada com Sucesso"}


async def get_sessions_for_lab(lab_id: str, db:AsyncSession) -> List[SessionResponse]:
    result = await db.execute(
        select(Session).where(Session.lab_id == lab_id).options(
            selectinload(Session.student),
            selectinload(Session.machine),
        )
    )
    sessions = result.scalars().all()

    if not sessions:
        raise HTTPException(status_code=404, detail="Nenhuma sessão foi encontrada.")

    return [
        SessionResponse(
            session_start=s.session_start.strftime("%d/%m/%Y %H:%M:%S"),
            student=StudentResponse(
                student_name=s.student.student_name,
                class_var=s.student.class_var,
            ),
            machine_name=s.machine.name
        )
        for s in sessions
    ]

async def get_sessions_for_student(student_id: int, db: AsyncSession) -> List[SessionResponse]:
    result = await db.execute(
        select(Session).where(Session.student_id == student_id).options(
            selectinload(Session.student),
            selectinload(Session.machine),
        )
    )
    sessions = result.scalars().all()

    if not sessions:
        raise HTTPException(status_code=404, detail="Nenhuma sessão foi encontrada para o estudante.")

    return [
        SessionResponse(
            session_start=s.session_start.strftime("%d/%m/%Y %H:%M:%S"),
            student=StudentResponse(
                student_name=s.student.student_name,
                class_var=s.student.class_var,
            ),
            machine_name=s.machine.name
        )
        for s in sessions
    ]


async def get_sessions_for_machine(machine_key: str, db: AsyncSession) -> List[SessionResponse]:
    result = await db.execute(
        select(Session).where(Session.machine_key == machine_key).options(
            selectinload(Session.student),
            selectinload(Session.machine),
        )
    )
    sessions = result.scalars().all()

    if not sessions:
        raise HTTPException(status_code=404, detail="Nenhuma sessão foi encontrada para esta máquina.")

    return [
        SessionResponse(
            session_start=s.session_start.strftime("%d/%m/%Y %H:%M:%S"),
            student=StudentResponse(
                student_name=s.student.student_name,
                class_var=s.student.class_var,
            ),
            machine_name=s.machine.name
        )
        for s in sessions
    ]

