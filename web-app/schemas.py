from pydantic import BaseModel

class User(BaseModel):
    name: str
    class_var: str
    password: str

class PcInfo(BaseModel):
    cpu_usage: float
    ram_usage: float
    cpu_temp: float


class MachineResponse(BaseModel):
    session_start: str
    user: User
    pc_info: PcInfo