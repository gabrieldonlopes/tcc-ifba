from pydantic import BaseModel

class User(BaseModel):
    name: str
    class_var: str
    password: str
