import requests as req 
import aiohttp
import os 
from dotenv import load_dotenv
from typing import List


from pydantic import ValidationError

from schemas import SessionCreate,SessionResponse,StudentResponse
from config import get_machine_key,get_local_config
from utils.pc_info import get_pc_info,get_session_start
load_dotenv()

WEB_API_KEY = os.getenv("WEB_API_KEY")
BASE_URL = os.getenv("BASE_URL")


url = f"{BASE_URL}/session"  
headers = {
    "api-key":WEB_API_KEY,
    "Content-Type": "application/json"  
}

# TODO: implementar tratamento de erros da api
def post_session(student_name: str,password: str,class_var: str) -> tuple[bool, str]:
    try:
        pc_info = get_pc_info()
        session_start = get_session_start()
        machine_key = get_machine_key()
        local_config = get_local_config()
        #print(pc_info,session_start,machine_key)
        
        new_session = SessionCreate(
            student_name=student_name,
            password=password,
            class_var=class_var,
            session_start=session_start,
            cpu_usage=pc_info.cpu_usage,
            ram_usage=pc_info.ram_usage,
            cpu_temp=pc_info.cpu_temp,
            lab_id=local_config.lab_id
        )
        
        response = req.post(
            url=f"{url}/new/{machine_key}",
            headers=headers,
            json=new_session.model_dump(),
            verify=False,
            timeout=10
        )
        response.raise_for_status()
        return True, "Configuração salva com sucesso"
    except req.exceptions.HTTPError as e:
            error_detail = e.response.json().get('detail', str(e))
            return False, error_detail  
    
def get_sessions_for_machine() -> List[SessionResponse] | None:
    response = req.get(f"{url}/machine/{get_machine_key()}", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        try:
            return [SessionResponse(**item) for item in data]
        except ValidationError as e:
            raise Exception(f"Dados inválidos da API: {e.errors()}")
    elif response.status_code == 404:
        return None
    else:
        raise Exception(f"Erro na requisição: {response.status_code}")