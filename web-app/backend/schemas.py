from pydantic import BaseModel

class User(BaseModel):
    name: str
    class_var: str
    password: str

class PcInfo(BaseModel):
    cpu_usage: float
    ram_usage: float
    cpu_temp: float

class MachineConfig(BaseModel):
    name:str
    motherboard: str
    memory: str
    storage: str
    state_cleanliness: str
    last_checked: str
    lab_id: str

class NewMachineConfig(MachineConfig):
    machine_key: str