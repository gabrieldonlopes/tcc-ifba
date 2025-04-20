from pydantic import BaseModel

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
    motherboard: str
    name:str
    memory: str
    storage: str
    state_cleanliness: str
    last_checked: str
    lab_id: str

class NewMachineConfig(MachineConfig):
    machine_key: str