import secrets
import json
import os 
import requests as req

from pydantic import ValidationError
from dotenv import load_dotenv
from typing import Optional,Union

from schemas import MachineConfig,NewMachineConfig,LocalConfig,LabInfo
from exceptions import MachineKeyAlreadyExists

load_dotenv()

# app_name = "InfoDomus"
# config_path = os.path.join(os.getenv("LOCALAPPDATA"), app_name, "config.json")
config_path = "./config.json" # opção apenas para testes

WEB_API_KEY: Optional[str] = os.getenv("WEB_API_KEY")
BASE_URL: Optional[str] = os.getenv("BASE_URL")


def create_machine_key() -> str:
    """
    Returns an existing machine key if found in config.json, otherwise generates a new one.
    The new key is NOT saved to config.json by this function.
    """
    key = get_machine_key()
    if not key:
        return secrets.token_hex(32)
    return key

def get_machine_key() -> Optional[str]:
    """Retrieves the machine key from config.json."""
    if not os.path.isfile(config_path):
        return None
    try:
        with open(config_path, "r", encoding='utf-8') as file:
            config_data = json.load(file)
        return config_data.get("machine_key")
    except (json.JSONDecodeError, FileNotFoundError):
        return None
    
def get_machine_config_from_api() -> Optional[MachineConfig]:
    """Retrieves machine configuration from the API."""
    machine_key = get_machine_key()
    if not machine_key:
        return None

    if not WEB_API_KEY or not BASE_URL:
        raise Exception(f"Dados inválidos: WEB_API_KEY e BASE_URL")

    headers = {
        "api-key": WEB_API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = req.get(f"{BASE_URL}/machine_config/{machine_key}", headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            try:
                return MachineConfig(**data)
            except ValidationError as e:
                raise Exception(f"Dados inválidos da API: {e.errors()}")
        elif response.status_code == 404:
            return None
        response.raise_for_status() 
    except req.exceptions.RequestException as e:
        raise Exception(f"Erro de comunicação com a API ao buscar configuração da máquina: {e}")
    return None 

def get_local_config() -> Optional[LocalConfig]:
    """Reads local configuration from config.json."""
    if not os.path.isfile(config_path):
        return None
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return LocalConfig(**data)
    except (json.JSONDecodeError, ValidationError, FileNotFoundError) as e:
        return None

def get_lab_info(lab_id: str) -> Optional[LabInfo]:
    """Retrieves laboratory information from the API."""
    if not WEB_API_KEY or not BASE_URL:
        raise Exception("Configuração crítica ausente: WEB_API_KEY e/ou BASE_URL não definidos.")
        
    headers = {
        "api-key": WEB_API_KEY,
        "Content-Type": "application/json"
    }
    try:
        response = req.get(
            url=f"{BASE_URL}/lab/{lab_id}",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return LabInfo(**data)
    except req.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            raise Exception("O laboratório não foi encontrado")
        raise Exception(f"Erro HTTP ao buscar informações do laboratório: {http_err}")
    except req.exceptions.RequestException as req_err:
        raise Exception(f"Erro de conexão ao buscar informações do laboratório: {req_err}")
    except ValidationError as val_err:
        raise Exception(f"Erro de validação nos dados do laboratório: {val_err.errors()}")
    except Exception as e: # Catch any other unexpected errors
        raise Exception(f"Erro ao processar dados do laboratório: {e}")

def write_local_info_to_json(local_config: LocalConfig, filename=config_path):
    """Writes the local configuration object to a JSON file."""
    if not hasattr(local_config, 'model_dump'):
        raise AttributeError("Objeto local_config inválido: método model_dump() não encontrado.")

    config_dict = local_config.model_dump()
    try:
        # Garante que o diretório exista
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "w", encoding='utf-8') as f:
            json.dump(config_dict, f, indent=4)
    except IOError as e:
        raise IOError(f"Erro de E/S ao salvar a configuração local no arquivo {filename}: {e}")
    except Exception as e:
        raise Exception(f"Erro inesperado ao salvar a configuração local no arquivo {filename}: {e}")


def save_local_config(machine_key: str, machine_config_data: Union[NewMachineConfig, MachineConfig]):
    """Saves local configuration based on machine and lab info."""
    try:
        # Ensure lab_id is present
        lab_id_val = getattr(machine_config_data, 'lab_id', None)
        if not lab_id_val:
            raise ValueError("ID do laboratório (lab_id) não encontrado na configuração da máquina.")

        lab_info = get_lab_info(lab_id=lab_id_val)
        if not lab_info: # Segurança adicional, embora get_lab_info deva levantar exceção antes
            raise ValueError(f"Não foi possível obter informações para o lab_id: {lab_id_val} (resposta inesperada).")

        # Ensure machine_name is present
        machine_name_val = getattr(machine_config_data, 'machine_name', 'DefaultMachineName')
        if not machine_name_val:
             raise ValueError("Nome da máquina (machine_name) não encontrado na configuração.")

        local_config_payload = {
            "machine_key": machine_key,
            "machine_name": machine_name_val,
            "lab_name": getattr(lab_info, 'lab_name'),
            "lab_id": getattr(lab_info, 'lab_id'),
            "classes": getattr(lab_info, 'classes')
        }
        current_local_config = LocalConfig(**local_config_payload)
        write_local_info_to_json(local_config=current_local_config)
    except (ValueError, AttributeError, IOError, Exception) as e:
        # Re-levanta a exceção para ser tratada por post_config_from_ui
        raise Exception(f"Falha ao salvar configuração local: {e}")


def post_config_from_ui(raw_data: dict) -> tuple[bool, str]:
    """Posts new or updates existing machine configuration from UI data."""
    if not WEB_API_KEY or not BASE_URL:
        return False, "WEB_API_KEY or BASE_URL is not configured."

    current_machine_key_from_file = get_machine_key()
    is_update_operation = bool(current_machine_key_from_file)

    headers = {
        "api-key": WEB_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        if is_update_operation and current_machine_key_from_file:
            # Update existing configuration
            machine_config_update_data = MachineConfig(**raw_data) # Validate raw_data
            response = req.patch(
                url=f"{BASE_URL}/machine_config/update/{current_machine_key_from_file}",
                headers=headers,
                json=machine_config_update_data.model_dump(),
                timeout=10
            )
            response.raise_for_status()
            save_local_config(machine_key=current_machine_key_from_file, machine_config_data=machine_config_update_data)
            return True, "Configuração atualizada com sucesso"
        else:
            # Create new configuration
            # `create_machine_key` will generate a new hex token if no config.json or key exists
            key_for_new_machine = create_machine_key()
            
            new_machine_payload = {"machine_key": key_for_new_machine, **raw_data}
            machine_config_new_data = NewMachineConfig(**new_machine_payload) # Validate

            response = req.post(
                url=f"{BASE_URL}/machine_config/new_machine",
                headers=headers,
                json=machine_config_new_data.model_dump(),
                timeout=10
            )
            # If server says key already exists (e.g. 409 Conflict)
            if response.status_code == 409: 
                raise MachineKeyAlreadyExists(f"Chave da máquina {key_for_new_machine} já existe no servidor (conflito ao tentar criar).")
            
            response.raise_for_status()
            save_local_config(machine_key=key_for_new_machine, machine_config_data=machine_config_new_data)
            return True, "Configuração salva com sucesso"

    except MachineKeyAlreadyExists as mkae:
        # This block is hit if POSTing a new key (is_update_operation was False)
        # resulted in a 409 or other explicit "key exists" error from the server.
        # We might want to attempt an update if the key reported as existing is one we can use.
        # The key that caused the conflict was `key_for_new_machine`.
        conflicting_key_str = str(mkae)
        try:
            # Ex: "A chave da máquina XYZ já existe no servidor."
            conflicting_key = conflicting_key_str.split(" ")[4] if " " in conflicting_key_str else None
            if not conflicting_key: # Fallback se a extração falhar
                 return False, f"Conflito de chave: {mkae}. Não foi possível extrair a chave para tentar atualização."

            update_payload = MachineConfig(**raw_data) 
            response = req.patch(
                url=f"{BASE_URL}/machine_config/update/{conflicting_key}",
                headers=headers,
                json=update_payload.model_dump(),
                timeout=10
            )
            response.raise_for_status()
            save_local_config(machine_key=conflicting_key, machine_config_data=update_payload)
            return True, f"Configuração atualizada com sucesso para a chave {conflicting_key} após conflito inicial."
        except req.exceptions.HTTPError as e_patch:
            error_detail = e_patch.response.json().get('detail', str(e_patch)) if e_patch.response else str(e_patch)
            return False, f"Falha ao tentar atualizar configuração após conflito de chave ({e_patch.response.status_code if e_patch.response else 'N/A'}): {error_detail}"
        except Exception as e_inner_patch: # Outros erros durante a tentativa de PATCH
            return False, f"Falha interna ao tentar atualizar configuração após conflito de chave: {str(e_inner_patch)}"
            
    except req.exceptions.HTTPError as e: # Erros HTTP das chamadas PATCH ou POST principais
        error_detail = e.response.json().get('detail', str(e)) if e.response else str(e)
        status_code_info = f" (status: {e.response.status_code})" if e.response else ""
        return False, f"Erro de API ao salvar configuração{status_code_info}: {error_detail}"
            
    except req.exceptions.RequestException as e: # Erros de conexão, timeout, etc.
        return False, f"Erro de comunicação com a API ao salvar configuração: {str(e)}"
        
    except ValidationError as e: # Erro de validação dos dados de entrada (raw_data)
        error_messages = [f"{'->'.join(map(str, err['loc']))}: {err['msg']}" for err in e.errors()]
        return False, f"Erro de validação nos dados fornecidos: {'; '.join(error_messages)}"
        
    except (IOError, AttributeError, ValueError, Exception) as e: # Erros de save_local_config ou outros inesperados
        return False, f"Erro ao processar ou salvar configuração: {str(e)}"