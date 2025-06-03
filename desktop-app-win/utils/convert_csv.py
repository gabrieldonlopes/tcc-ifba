from pathlib import Path
from pydantic import BaseModel
import csv
from typing import List
import pandas as pd

from schemas import MachineResponse
def get_downloads_path() -> Path:
    home = Path.home()    
    if (home / "Downloads").exists():  # Windows e alguns Linux
        return home / "Downloads"

def machine_responses_to_csv(responses: List[MachineResponse], filename: str):
    if not responses:
        return
    
    downloads_path = get_downloads_path()
    
    file_path = downloads_path / filename
    
    # "aplainando os dados"
    flat_data = []
    for response in responses:
        flat_item = {
            "session_start": response.session_start,
            "user_name": response.user.name,
            "user_class_var": response.user.class_var,
            "cpu_usage": response.pc_info.cpu_usage,
            "ram_usage": response.pc_info.ram_usage,
            "cpu_temp": response.pc_info.cpu_temp
        }
        flat_data.append(flat_item)
    
    df = pd.DataFrame(flat_data)
    df.to_csv(file_path, index=False)
    
