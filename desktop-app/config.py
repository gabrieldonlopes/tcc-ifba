import secrets
import json
import os 
import requests as req

from dotenv import load_dotenv
from typing import Optional

from schemas import MachineConfig,NewMachineConfig
from exceptions import MachineKeyAlreadyExists
#TODO: adicionar operações async

load_dotenv()

WEB_API_KEY = os.getenv("WEB_API_KEY")
BASE_URL = os.getenv("BASE_URL")


def create_machine_key():
    if get_machine_key(): # verificacao de chave
        raise MachineKeyAlreadyExists

    key = secrets.token_hex(32) # cria uma chave para machine
    config = {"machine_key":key}

    with open("config.json","w") as file: # escreve a chave em config.json
        json.dump(config,file,indent=4)
    print("chave criada com sucesso")

def get_machine_key() -> Optional[str]:
    try:
        with open("config.json","r") as file:
            config = json.load(file)
    except (FileNotFoundError):
        return None
    except json.JSONDecodeError: # caso ocorra algum erro na leitura 
        return None
    return config.get("machine_key")

def get_config():
    pass

def post_config(machine_config: MachineConfig):
    try:
        create_machine_key()
        machine_key = get_machine_key()
        
        data = machine_config.model_dump()
        new_machine_config = NewMachineConfig(machine_key=machine_key,**data)
        
        url = f"{BASE_URL}/config/new_machine"  
        headers = {
            "api-key": WEB_API_KEY,
            "Content-Type": "application/json"
        }

        headers.pop("machine_key") # machine key não é necessario para essa aplicacao
        req.post(url=url,headers=headers,json=new_machine_config.model_dump(), verify=False)
    
    except(MachineKeyAlreadyExists):
        MACHINE_KEY = get_machine_key()
        url = f"{BASE_URL}/config/config_machine"  
        headers = {
            "api-key": WEB_API_KEY,
            "machine_key": MACHINE_KEY,
            "Content-Type": "application/json"
        }
    

        req.post(url=url,headers=headers,json=machine_config.model_dump(),verify=False)
        
        