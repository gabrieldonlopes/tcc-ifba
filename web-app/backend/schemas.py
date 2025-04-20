from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, BeforeValidator, field_validator
from models import StateCleanliness

def parse_last_checked(value: str) -> datetime:
    if isinstance(value, datetime):
        return value
    try:
        return datetime.strptime(value, "%d-%m-%Y")
    except ValueError:
        raise ValueError("Formato de data inválido. Use DD-MM-AAAA")

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
    last_checked: Annotated[datetime, BeforeValidator(parse_last_checked)]
    lab_id: str
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%d-%m-%Y"),
            StateCleanliness: lambda v: v.value
        }

class NewMachineConfig(MachineConfig):
    machine_key: str
