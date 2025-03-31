import requests as req 
import os 
from dotenv import load_dotenv

from schemas import User
from typing import List

load_dotenv()
WEB_API_KEY = os.getenv("WEB_API_KEY")

url = "http://localhost:8000/data"
headers = {
    "api-key":WEB_API_KEY,
    "Content-Type": "application/json"  
}

#TODO: adicionar tratamento de dados
def send_user(name,class_var,password):
    
    # TODO: separar essa transformação de objeto para controller
    # TODO: adicionar verificação de usuario
    new_user = User(name=name,class_var=class_var,password=password)
    
    response = req.post(url=url,headers=headers,json=new_user.model_dump(),verify=False)
    #print(response.status,response.text)

def get_data() -> List[User]:
    response = req.get(url=url)
    users_data = response.json()
    return [User(**user) for user in users_data]
