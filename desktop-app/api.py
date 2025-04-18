import requests as req 
import os 
from dotenv import load_dotenv
from typing import List

from utils.data_handler import transform_reponse
from schemas import Session, User
from config import get_machine_key
load_dotenv()

WEB_API_KEY = os.getenv("WEB_API_KEY")
BASE_URL = os.getenv("BASE_URL")
MACHINE_KEY = get_machine_key()

url = f"{BASE_URL}/data"  
headers = {
    "api-key":WEB_API_KEY,
    "machine_key":MACHINE_KEY,
    "Content-Type": "application/json"  
}

#TODO: adicionar tratamento de dados
def post_user(new_user:User):
    machine_response = transform_reponse(new_user)
    # TODO: separar essa transformação de objeto para controller
    # TODO: adicionar verificação de usuario
    req.post(url=url,headers=headers,json=machine_response.model_dump(),verify=False)

def get_all_sessions() -> List[Session]:
    response = req.get(url=url)
    sessions_data = response.json()
    return [Session(**session) for session in sessions_data]

