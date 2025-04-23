from datetime import datetime
from typing import List
from pydantic import BaseModel, field_validator
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
    last_checked: str  # String no formato DD-MM-AAAA
    lab_id: str

    @field_validator('last_checked')
    def validate_date_format(cls, value):
        try:
            datetime.strptime(value, "%d-%m-%Y")
            return value
        except ValueError:
            raise ValueError("Formato de data inválido. Use DD-MM-AAAA")

    class Config:
        json_encoders = {
            StateCleanliness: lambda v: v.value,
            datetime: lambda v: v.strftime("%d-%m-%Y") if v else None
        }

class NewMachineConfig(MachineConfig):
    machine_key: str

class LabCreate(BaseModel):
    lab_id: str
    name: str
    classes: str

class LabResponse(BaseModel):
    name: str
    classes: List[str]

