from sqlalchemy import Integer, String, Boolean, Date, DateTime, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column,relationship, DeclarativeBase, validates
from sqlalchemy.ext.asyncio import AsyncAttrs

from datetime import datetime

class Base(AsyncAttrs, DeclarativeBase): # atualização de models para operações assincronas
    pass

from enum import Enum
from sqlalchemy import Enum as SqlEnum

class StateCleanliness(str, Enum):
    BOM = "BOM"
    REGULAR = "REGULAR"
    URGENTE = "URGENTE"

user_lab_association = Table(
    "user_lab_association",
    Base.metadata,
    Column("user_id", ForeignKey("User.user_id"), primary_key=True),
    Column("lab_id", ForeignKey("Lab.lab_id"), primary_key=True)
)

class Machine(Base):
    __tablename__ = "Machine"
    
    machine_key: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    motherboard: Mapped[str] = mapped_column(String(100))
    memory: Mapped[str] = mapped_column(String(100))
    storage: Mapped[str] = mapped_column(String(100))
    state_cleanliness: Mapped[StateCleanliness] = mapped_column(SqlEnum(StateCleanliness))
    last_checked: Mapped[datetime] = mapped_column(Date)

    lab_id: Mapped[str] = mapped_column(ForeignKey("Lab.lab_id"))  
    lab: Mapped["Lab"] = relationship("Lab", back_populates="machines")
    
    sessions: Mapped[list["Session"]] = relationship("Session", back_populates="machine")
    @validates("last_checked")
    def validate_session_start(self, key, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%d/%m/%Y")
            except ValueError as e:
                raise ValueError("Formato de data/hora inválido. Use DD/MM/AAAA") from e
        elif isinstance(value, datetime):
            return value
        else:
            raise TypeError("last_checked deve ser datetime ou string no formato válido.")
    
class Student(Base):
    __tablename__ = "Student"

    student_id: Mapped[int] = mapped_column(Integer,primary_key=True)
    student_name: Mapped[str] = mapped_column(String(100))
    password_hash: Mapped[str] = mapped_column(String(255))  
    class_var: Mapped[str] = mapped_column(String(50))

    sessions: Mapped[list["Session"]] = relationship("Session", back_populates="student")

class Lab(Base):    
    __tablename__ = "Lab"

    lab_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    lab_name: Mapped[str] = mapped_column(String(100))
    classes: Mapped[str] = mapped_column(String(50))

    users: Mapped[list["User"]] = relationship(
        secondary=user_lab_association,
        back_populates="labs"
    )
    machines: Mapped[list["Machine"]] = relationship("Machine", back_populates="lab")
    sessions: Mapped[list["Session"]] = relationship("Session", back_populates="lab")


class Session(Base):
    __tablename__ = "Session"

    session_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_start: Mapped[datetime] = mapped_column(DateTime)

    machine_key: Mapped[str] = mapped_column(ForeignKey("Machine.machine_key"))
    machine: Mapped["Machine"] = relationship("Machine", back_populates="sessions")

    student_id: Mapped[int] = mapped_column(ForeignKey("Student.student_id"))
    student: Mapped["Student"] = relationship("Student", back_populates="sessions")

    lab_id: Mapped[str] = mapped_column(ForeignKey("Lab.lab_id"))
    lab: Mapped["Lab"] = relationship("Lab", back_populates="sessions")

    @validates("session_start")
    def validate_session_start(self, key, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%d/%m/%Y %H:%M:%S")
            except ValueError as e:
                raise ValueError("Formato de data/hora inválido. Use DD/MM/AAAA HH:MM:SS") from e
        elif isinstance(value, datetime):
            return value
        else:
            raise TypeError("session_start deve ser datetime ou string no formato válido.")

class User(Base):
    __tablename__ = "User"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))  
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    labs: Mapped[list["Lab"]] = relationship(
        secondary=user_lab_association,
        back_populates="users"
    )
    

