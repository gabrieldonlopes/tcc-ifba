import secrets
import aiohttp
import json
import os 
import requests as req
import asyncio

from pydantic import ValidationError
from dotenv import load_dotenv
from typing import Optional

from schemas import MachineConfig,NewMachineConfig,LocalConfig,LabInfo
from exceptions import MachineKeyAlreadyExists
#TODO: adicionar operações async

load_dotenv()

WEB_API_KEY = os.getenv("WEB_API_KEY")
BASE_URL = os.getenv("BASE_URL")

def transform_model_machine_config():
    pass

def create_machine_key() -> str:
    if get_machine_key(): # verificacao de chave
        raise MachineKeyAlreadyExists

    return secrets.token_hex(32) # cria uma chave para machine

def get_machine_key() -> Optional[str]:
    try:
        with open("config.json","r") as file:
            config = json.load(file)
    except (FileNotFoundError):
        return None
    except json.JSONDecodeError: # caso ocorra algum erro na leitura 
        return None
    return config.get("machine_key")

async def get_machine_config() -> MachineConfig | None:
    machine_key = get_machine_key()
    headers = {
        "api-key": WEB_API_KEY,
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/machine_config/{machine_key}",headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                try:
                    return MachineConfig(**data)
                except ValidationError as e:
                    raise Exception(f"Dados inválidos da API: {e.errors()}")
            elif response.status == 404:
                return None
            raise Exception(f"Erro na requisição: {response.status}")
        
def get_local_config()->LocalConfig:
    if not os.path.isfile("config.json"):
        return None
    with open("config.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
        return LocalConfig(**data)

def get_lab_info(lab_id:str)->LabInfo:
    headers = {
        "api-key": WEB_API_KEY,
        "Content-Type": "application/json"
    }
    response = req.get(
        url=f"{BASE_URL}/lab/{lab_id}",
        headers=headers,
        verify=False,
        timeout=10
        )
    
    if response.status_code != 200:
        raise Exception("O laboratório não foi encontrado")

    try:
        data = response.json()
        return LabInfo(**data)
    except Exception as e:
        raise Exception(f"Erro ao processar dados do laboratório: {e}")

def write_local_info_to_json(local_config: LocalConfig, filename="config.json"):
    config_dict = local_config.model_dump()
    try:
        with open(filename, "w") as f:
            json.dump(config_dict, f, indent=4)
        print(f"Configuração salva com sucesso no arquivo {filename}.")
    except Exception as e:
        print(f"Erro ao salvar a configuração: {e}")

def save_local_config(machine_key:str,machine_config:MachineConfig):
    lab_info = get_lab_info(lab_id=machine_config.lab_id)

    local_config = LocalConfig(
        machine_key=machine_key,
        machine_name=machine_config.machine_name,
        lab_name=lab_info.lab_name,   # usando colchetes
        classes=lab_info.classes
    )
    write_local_info_to_json(local_config=local_config)

async def post_config_from_ui(raw_data: dict) -> tuple[bool, str]:
    try:
        machine_key = create_machine_key()

        machine_config = NewMachineConfig(machine_key=machine_key, **raw_data)
        print(machine_config.model_dump())
        response = req.post(
            url=f"{BASE_URL}/machine_config/new_machine",
            headers={
                "api-key": WEB_API_KEY,
                "Content-Type": "application/json"
            },
            json=machine_config.model_dump(),
            verify=False,
            timeout=10
        )

        # salva informações básicas sobre a máquina
        save_local_config(machine_key=machine_key,machine_config=machine_config)
        response.raise_for_status()
        return True, "Configuração salva com sucesso"

    except req.exceptions.HTTPError as e:
            error_detail = e.response.json().get('detail', str(e))
            return False, error_detail    
    except MachineKeyAlreadyExists:
        try:
            machine_key = get_machine_key()
                    
            response = req.patch(
                url=f"{BASE_URL}/machine_config/update/{machine_key}",
                headers={
                    "api-key": WEB_API_KEY,
                        "Content-Type": "application/json"
                    },
                json=MachineConfig(**raw_data).model_dump(),
                verify=False,
                timeout=10
            )
                
            response.raise_for_status()

            # salva informações básicas sobre a máquina
            save_local_config(machine_key=machine_key,machine_config=machine_config)
            return True, "Configuração atualizada com sucesso"
            
        except req.exceptions.HTTPError as e:
            error_detail = e.response.json().get('detail', str(e))
            return False, error_detail
            
        except Exception as e:
            return False, f"Falha ao atualizar: {str(e)}"

    except req.exceptions.RequestException as e:
        return False, f"Erro de conexão: {str(e)}"
        
    except ValidationError as e:
        error_messages = []
        for error in e.errors():
            field = "->".join(map(str, error['loc']))
            error_messages.append(f"{field}: {error['msg']}")
        return False, f"Erro de validação: {'; '.join(error_messages)}"
        
    except Exception as e:
        return False, f"Erro inesperado: {str(e)}"