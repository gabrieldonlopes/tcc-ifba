from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from typing import List

from models import Machine, Session,SystemMetrics,Lab,Student
from schemas import SessionCreate,SessionResponse
from student.student_handler import verify_student

async def post_new_session(machine_key: str, session: SessionCreate, db: AsyncSession):
    # Verifica se a máquina existe
    machine_result = await db.execute(select(Machine).filter(Machine.machine_key == machine_key))
    machine_config_obj = machine_result.scalars().first()
    
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

    if not student_obj:
        raise HTTPException(status_code=404, detail="Estudante não encontrado.")
    
    # Criar a sessão
    db_session = Session(
        session_start=session.session_start,
        machine_key=machine_key,
        student_id=student_obj.student_id,
        lab_id=machine_config_obj.lab_id
    )
    
    # Criar as métricas do sistema
    db_system_metrics = SystemMetrics(
        cpu_usage=session.cpu_usage,
        ram_usage=session.ram_usage,
        cpu_temp=session.cpu_temp,
        session=db_session 
    )
    
    try:
        # Adicionando e comitando tanto a sessão quanto as métricas
        db.add(db_session)
        db.add(db_system_metrics)
        await db.commit()
        await db.refresh(db_session)
        await db.refresh(db_system_metrics)
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar sessão. Detalhes: {str(e)}",
        )

    return {"message": "Sessão registrada com sucesso!"}


async def get_sessions_for_lab(lab_id: str, db: AsyncSession) -> List[SessionResponse]:
    lab_result = await db.execute(
        select(Lab).where(Lab.lab_id == lab_id)
    )
    lab_obj = lab_result.scalars().first()
    
    if not lab_obj:
        raise HTTPException(status_code=404, detail="Nenhuma lab foi encontrado.")
    
    result = await db.execute(
        select(Session).where(Session.lab == lab_obj).options(
            selectinload(Session.student),
            selectinload(Session.machine),
            selectinload(Session.system_metrics)  # Carrega as métricas do sistema
        )
    )
    sessions = result.scalars().all()

    if not sessions:
        raise HTTPException(status_code=404, detail="Nenhuma sessão foi encontrada.")

    return [
        SessionResponse(
            session_start=s.session_start.strftime("%d/%m/%Y %H:%M:%S"),
            student_name=s.student.student_name,
            class_var=s.student.class_var,
            cpu_usage=s.system_metrics.cpu_usage if s.system_metrics else None,  # Acessando as métricas associadas
            ram_usage=s.system_metrics.ram_usage if s.system_metrics else None,
            cpu_temp=s.system_metrics.cpu_temp if s.system_metrics else None,
            machine_name=s.machine.machine_name,
            lab_name=lab_obj.lab_name  # Acessando o nome do laboratório
        )
        for s in sessions
    ]


async def get_sessions_for_student(student_id: int, db: AsyncSession) -> List[SessionResponse]:
    student_result = await db.execute(
        select(Student).where(Student.student_id==student_id)
    )
    student_obj = student_result.scalars().first()
    
    if not student_obj:
        raise HTTPException(status_code=404, detail="Nenhum estudante foi encontrado.")
    
    
    result = await db.execute(
        select(Session).where(Session.student == student_obj).options(
            selectinload(Session.machine),
            selectinload(Session.system_metrics),  # Carrega as métricas do sistema
            selectinload(Session.lab)
        )
    )
    sessions = result.scalars().all()

    if not sessions:
        raise HTTPException(status_code=404, detail="Nenhuma sessão foi encontrada para o estudante.")

    return [
        SessionResponse(
            session_start=s.session_start.strftime("%d/%m/%Y %H:%M:%S"),
            student_name=s.student.student_name,
            class_var=s.student.class_var,
            cpu_usage=s.system_metrics.cpu_usage if s.system_metrics else None,  # Adicionando as métricas
            ram_usage=s.system_metrics.ram_usage if s.system_metrics else None,
            cpu_temp=s.system_metrics.cpu_temp if s.system_metrics else None,
            machine_name=s.machine.machine_name,
            lab_name=s.lab.lab_name  # Nome do laboratório associado à sessão
        )
        for s in sessions
    ]



async def get_sessions_for_machine(machine_key: str, db: AsyncSession) -> List[SessionResponse]:
    # verifica a existência da máquina
    machine_result = await db.execute(
        select(Machine).where(Machine.machine_key==machine_key)
    )
    machine_obj = machine_result.scalars().first()
    if not machine_obj:
        raise HTTPException(status_code=404, detail="Máquina não foi encontrada.")

    result = await db.execute(
        select(Session).where(Session.machine == machine_obj).options(
            selectinload(Session.student),
            selectinload(Session.system_metrics),  # Carrega as métricas do sistema
            selectinload(Session.lab)
        )
    )
    sessions = result.scalars().all()

    if not sessions:
        raise HTTPException(status_code=404, detail="Nenhuma sessão foi encontrada para esta máquina.")

    return [
        SessionResponse(
            student_name=s.student.student_name,
            class_var=s.student.class_var,
            session_start=s.session_start.strftime("%d/%m/%Y %H:%M:%S"),
            cpu_usage=s.system_metrics.cpu_usage,  # Adicionando as métricas
            ram_usage=s.system_metrics.ram_usage, 
            cpu_temp=s.system_metrics.cpu_temp,
            machine_name=machine_obj.machine_name,
            lab_name=s.lab.lab_name  # Nome do laboratório associado à sessão
        )
        for s in sessions
    ]


