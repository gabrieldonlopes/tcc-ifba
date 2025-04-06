from pydantic import BaseModel

class User(BaseModel): # usada para login do estudante
    name: str
    class_var: str
    cpf: str

class PcInfo(BaseModel): # informações do computador no momento de login
    cpu_usage: float
    ram_usage: float
    cpu_temp: float

class Session(BaseModel):
    machine_id: str
    session_start: str
    user: User
    pc_info: PcInfo

class MachineConfig(BaseModel):
    motherboard: str
    memory: str
    storage: str
    state_cleanliness: str

class NewMachineConfig(MachineConfig):
    machine_key: str