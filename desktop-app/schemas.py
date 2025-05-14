from pydantic import BaseModel, field_serializer, field_validator
from datetime import datetime
from typing import List
from enum import Enum

def parse_last_checked_date(value: str) -> datetime:
    try:
        return datetime.strptime(value, "%d/%m/%Y")
    except ValueError:
        raise ValueError("Formato inválido. Use DD/MM/YYYY")
    
class StateCleanliness(str, Enum):
    BOM = "BOM"
    REGULAR = "REGULAR"
    URGENTE = "URGENTE"

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

class SessionResponse(SessionCreate):
    machine_name:str
    lab_name:str

class PcInfo(BaseModel):
    cpu_usage: float
    ram_usage: float
    cpu_temp: float

class LabInfo(BaseModel):
    lab_name: str
    classes: List[str]

class MachineConfig(BaseModel):
    machine_name: str
    motherboard: str
    memory: str
    storage: str
    state_cleanliness: StateCleanliness
    last_checked: str  # String no formato DD/MM/AAAA
    lab_id: str

    @field_validator('last_checked')
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

# model utilizado para guardar as informações 
class LocalConfig(BaseModel):
    machine_key: str
    machine_name: str
    lab_name:str
    classes:List[str]