from pydantic import BaseModel, BeforeValidator, field_serializer
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
    name:str
    motherboard: str
    memory: str
    storage: str
    state_cleanliness: StateCleanliness
    last_checked: str
    lab_id: str
    #@field_serializer('last_checked')
    #def serialize_last_checked(self, value: datetime) -> str:
    #    return value.strftime("%d-%m-%Y")

    #@field_serializer('state_cleanliness')
    #def serialize_clean_state(self, value: StateCleanliness) -> str:
    #    return value.value

   # def model_dump(self, **kwargs):
    #    return {
     #       "name": self.name,
      #      "motherboard": self.motherboard,
       #     "memory": self.memory,
        #    "storage": self.storage,
         #   "state_cleanliness": self.state_cleanliness.value,  # Usa .value do Enum
          #  "last_checked": self.serialize_last_checked(self.last_checked),
           # "lab_id": self.lab_id
        #}
class NewMachineConfig(MachineConfig):
    machine_key: str