from passlib.context import CryptContext
from fastapi import HTTPException, status

from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession 

from models import Student

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_student(student_name: str, class_var: str, db: AsyncSession) -> Student|None:
    result = await db.execute(select(Student).filter(Student.student_name == student_name.lower()))
    student_obj = result.scalars().first()
    if not student_obj:
        return None
    if student_obj.student_name == student_name.lower() and student_obj.class_var == class_var:
        return student_obj
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário, classe ou senha incorretos.",
        )

async def register_student(student_name: str, password: str, class_var: str, db: AsyncSession) -> Student:    
    hashed_password = get_password_hash(password)
    db_student = Student(
        student_name=student_name.lower(),
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
    student_obj = await get_student(student_name=student_name, class_var=class_var, db=db)

    if isinstance(student_obj,Student):
        if not verify_password(password, student_obj.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário, classe ou senha incorretos.",
            )
        return student_obj
    else:    
        return await register_student(student_name=student_name, password=password, class_var=class_var, db=db)
    
    