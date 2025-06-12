from datetime import datetime
from typing import List,Optional
from pydantic import BaseModel, field_validator
from models import StateCleanliness

# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str | None = None
    class Config:
        from_attributes = True

class UserInDB(UserResponse):
    hashed_password: str

class PcInfo(BaseModel):
    cpu_usage: float
    ram_usage: float
    cpu_temp: float

class MachineConfig(BaseModel):
    machine_name: str
    motherboard: str
    memory: str
    storage: str
    state_cleanliness: StateCleanliness
    last_checked: str  # String no formato DD/MM/AAAA
    lab_id: str

    @field_validator('last_checked',mode='before')
    def validate_date_format(cls, value):
        try:
            datetime.strptime(value, "%d/%m/%Y")
            return value
        except ValueError:
            raise ValueError("Formato de data inválido. Use DD/MM/AAAA")

    class Config:
        json_encoders = {
            StateCleanliness: lambda v: v.value,
            datetime: lambda v: v.strftime("%d/%m/%Y") if v else None
        }

class NewMachineConfig(MachineConfig):
    machine_key: str    

class MachineConfigResponse(BaseModel):
    machine_key: str
    motherboard: str
    machine_name: str
    state_cleanliness: StateCleanliness
    last_checked: str  # String no formato DD/MM/AAAA
    
    @field_validator('last_checked',mode='before')
    def validate_date_format(cls, value):
        try:
            datetime.strptime(value, "%d/%m/%Y")
            return value
        except ValueError:
            raise ValueError("Formato de data inválido. Use DD/MM/AAAA")

    class Config:
        json_encoders = {
            StateCleanliness: lambda v: v.value,
            datetime: lambda v: v.strftime("%d/%m/%Y") if v else None
        }

class LabCreate(BaseModel):
    lab_id: str
    lab_name: str
    classes: str

class LabUpdate(BaseModel):
    lab_name: Optional[str] = None
    classes: Optional[str] = None

class LabResponse(BaseModel):
    lab_name: str
    classes: List[str]
    machine_count: int
    student_count: int
    user_count: int

class LabResponseUser(BaseModel):
    lab_name: str
    classes: List[str]
    lab_id: str

class StudentResponse(BaseModel):
    student_name: str
    class_var: str

class SessionCreate(BaseModel):
    student_name: str
    password: str
    class_var: str
    session_start: str  # Formato: DD/MM/AAAA HH:MM:SS
    # métricas do sistema
    cpu_usage: float
    ram_usage: float
    cpu_temp: float
    lab_id: str

    @field_validator('session_start')
    def validate_datetime_format(cls, value):
        try:
            datetime.strptime(value, "%d/%m/%Y %H:%M:%S")
            return value
        except ValueError:
            raise ValueError("Formato de data/hora inválido. Use DD/MM/AAAA HH:MM:SS")

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%d/%m/%Y %H:%M:%S") if v else None
        }

class SessionResponse(BaseModel):
    student_name: str
    class_var: str
    session_start: str  # Formato: DD/MM/AAAA HH:MM:SS
    # métricas do sistema
    cpu_usage: float
    ram_usage: float
    cpu_temp: float
    machine_name:str
    lab_name: str

    @field_validator('session_start')
    def validate_datetime_format(cls, value):
        try:
            datetime.strptime(value, "%d/%m/%Y %H:%M:%S")
            return value
        except ValueError:
            raise ValueError("Formato de data/hora inválido. Use DD/MM/AAAA HH:MM:SS")

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%d/%m/%Y %H:%M:%S") if v else None
        }
