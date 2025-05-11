from passlib.context import CryptContext
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from models import Machine, Session, Student
from schemas import SessionCreate  # <- modelo Pydantic para entrada de dados

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_student(name: str, class_var: str, db: AsyncSession) -> Student | None:
    result = await db.execute(select(Student).filter(Student.student_name == name.lower()))
    student_obj = result.scalars().first()
    
    if student_obj.student_name == name.lower() and student_obj.class_var == class_var:
        return student_obj
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário, classe ou senha incorretos.",
        )

async def register_student(name: str, password: str, class_var: str, db: AsyncSession) -> Student:    
    hashed_password = get_password_hash(password)
    db_student = Student(
        student_name=name.lower(),
        password_hash=hashed_password,
        class_var=class_var,
    )
    try:
        db.add(db_student)
        await db.commit()
        await db.refresh(db_student)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao criar estudante. Tente novamente.",
        )
    return db_student

async def verify_student(student_name: str, password: str, class_var: str, db: AsyncSession) -> Student:
    student_obj = await get_student(name=student_name, class_var=class_var, db=db)
    if student_obj:
        if not verify_password(password, student_obj.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário, classe ou senha incorretos.",
            )
        return student_obj
    else:
        return await register_student(name=student_name, password=password, class_var=class_var, db=db)

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

    db_session = Session(
        session_start=session.session_start,
        machine_key=machine_key,
        student_id=student_obj.student_id
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
