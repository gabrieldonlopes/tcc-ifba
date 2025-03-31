import psutil
from datetime import datetime

def get_session_start():
    session_start = datetime.now()
    return session_start.strftime("%H:%M:%S %d/%m/%Y")

def get_pc_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    ram_usage = memory.percent

    try:
        temps = psutil.sensors_temperatures()
        cpu_temp = temps["coretemp"][0].current if "coretemp" in temps else "Não disponível"
    except AttributeError:
        cpu_temp = "Não disponível"
    return {
        "cpu_usage": cpu_usage,
        "ram_usage": ram_usage,
        "cpu_temp": cpu_temp
    }
