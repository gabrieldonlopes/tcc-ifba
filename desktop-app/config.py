import secrets
import aiohttp
import json
import os 
import requests as req
import asyncio

from pydantic import ValidationError
from dotenv import load_dotenv
from typing import Optional

from schemas import MachineConfig,NewMachineConfig
from exceptions import MachineKeyAlreadyExists
#TODO: adicionar operações async

load_dotenv()

WEB_API_KEY = os.getenv("WEB_API_KEY")
BASE_URL = os.getenv("BASE_URL")

def transform_model_machine_config():
    pass

def create_machine_key():
    if get_machine_key(): # verificacao de chave
        raise MachineKeyAlreadyExists

    key = secrets.token_hex(32) # cria uma chave para machine
    config = {"machine_key":key}

    with open("config.json","w") as file: # escreve a chave em config.json
        json.dump(config,file,indent=4)
    print("machine_key criada com sucesso")

def get_machine_key() -> Optional[str]:
    try:
        with open("config.json","r") as file:
            config = json.load(file)
    except (FileNotFoundError):
        return None
    except json.JSONDecodeError: # caso ocorra algum erro na leitura 
        return None
    return config.get("machine_key")

async def get_config() -> MachineConfig | None:
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
        

def post_config_from_ui(raw_data: dict) -> tuple[bool, str]:
    try:
        create_machine_key()
        machine_config = NewMachineConfig(machine_key=get_machine_key(), **raw_data)
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
        
        # Tratamento específico para status 400
        if response.status_code == 400:
            error_detail = response.json().get('detail', 'Máquina já registrada')
            return False, error_detail
        
        response.raise_for_status()
        return True, "Configuração salva com sucesso"

    except req.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            try:
                error_detail = e.response.json().get('detail', str(e))
                return False, error_detail
            except ValueError:
                return False, f"Erro 400: {str(e)}"
        return False, f"Erro HTTP {e.response.status_code}: {str(e)}"
    
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
            
            if response.status_code == 400:
                error_detail = response.json().get('detail', 'Erro ao atualizar')
                return False, error_detail
                
            response.raise_for_status()
            return True, "Configuração atualizada com sucesso"
            
        except req.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                error_detail = e.response.json().get('detail', str(e))
                return False, error_detail
            return False, f"Erro ao atualizar: {str(e)}"
            
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