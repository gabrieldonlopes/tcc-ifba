from pydantic import BaseModel, field_serializer, field_validator
from datetime import datetime
from typing import Annotated
from enum import Enum

def parse_last_checked_date(value: str) -> datetime:
    try:
        return datetime.strptime(value, "%d-%m-%Y")
    except ValueError:
        raise ValueError("Formato inválido. Use DD-MM-YYYY")
    
class StateCleanliness(str, Enum):
    BOM = "BOM"
    REGULAR = "REGULAR"
    URGENTE = "URGENTE"

class User(BaseModel): # usada para login do estudante
    name: str
    class_var: str
    password: str

class PcInfo(BaseModel): # informações do computador no momento de login
    cpu_usage: float
    ram_usage: float
    cpu_temp: float

class Session(BaseModel):
    session_start: str
    user: User
    pc_info: PcInfo

class MachineConfig(BaseModel):
    name: str
    motherboard: str
    memory: str
    storage: str
    state_cleanliness: StateCleanliness
    last_checked: str  # Já está como string
    lab_id: str

    @field_validator('state_cleanliness', mode='before')
    def validate_clean_state(cls, value):
        if isinstance(value, str):
            try:
                return StateCleanliness(value)
            except ValueError:
                raise ValueError(f"Estado inválido. Use: {[e.value for e in StateCleanliness]}")
        return value
   
        
class NewMachineConfig(MachineConfig):
    machine_key: str