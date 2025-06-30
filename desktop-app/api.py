import requests as req 
import aiohttp
import os 
from dotenv import load_dotenv
from typing import List


from pydantic import ValidationError

from schemas import SessionCreate,SessionResponse,StudentResponse
from config import get_machine_key
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

        print(pc_info,session_start,machine_key)
        
        new_session = SessionCreate(
            student_name=student_name,
            password=password,
            class_var=class_var,
            session_start=session_start,
            cpu_usage=pc_info.cpu_usage,
            ram_usage=pc_info.ram_usage,
            cpu_temp=pc_info.cpu_temp,
            lab_id="LAB01" # TODO: corrigir isso aqui
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
    
async def get_sessions_for_machine() -> List[SessionResponse]:
    #response = req.get(url=url)
    #sessions_data = response.json()
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/machine/{get_machine_key()}",headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                try:
                    return[
                        SessionResponse(
                            session_start=s.session_start.strftime("%d/%m/%Y %H:%M:%S"),
                            student=StudentResponse(
                                student_name=s.student.student_name,
                                class_var=s.student.class_var,
                            ),
                            machine_name=s.machine.machine_name
                        )
                        for s in data
                    ]
                except ValidationError as e:
                    raise Exception(f"Dados inválidos da API: {e.errors()}")
            elif response.status == 404:
                return None
            raise Exception(f"Erro na requisição: {response.status}")

def get_all_sessions():
    return ""
