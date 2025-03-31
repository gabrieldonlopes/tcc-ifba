import requests as req 
import os 
from dotenv import load_dotenv

from schemas import MachineResponse, User
from typing import List

from utils.data_handler import transform_reponse

load_dotenv()
WEB_API_KEY = os.getenv("WEB_API_KEY")

url = "http://localhost:8000/data"  
headers = {
    "api-key":WEB_API_KEY,
    "Content-Type": "application/json"  
}

#TODO: adicionar tratamento de dados
def post_user(new_user:User):
    machine_response = transform_reponse(new_user)
    # TODO: separar essa transformação de objeto para controller
    # TODO: adicionar verificação de usuario
    response = req.post(url=url,headers=headers,json=machine_response.model_dump(),verify=False)

def get_users() -> List[User]:
    response = req.get(url=url)
    users_data = response.json()
    return [User(**user) for user in users_data]
