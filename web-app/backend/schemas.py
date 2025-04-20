from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, BeforeValidator, field_validator
from models import StateCleanliness

class User(BaseModel):
    name: str
    class_var: str
    password: str

class PcInfo(BaseModel):
    cpu_usage: float
    ram_usage: float
    cpu_temp: float

class MachineConfig(BaseModel):
    name: str
    motherboard: str
    memory: str
    storage: str
    state_cleanliness: StateCleanliness
    last_checked: str  # Alterado para string
    lab_id: str

    class Config:
        json_encoders = {
            StateCleanliness: lambda v: v.value
        }

class NewMachineConfig(MachineConfig):
    machine_key: str
