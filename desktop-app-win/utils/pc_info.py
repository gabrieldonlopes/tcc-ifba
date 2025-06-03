from datetime import datetime
from pydantic import BaseModel
import psutil
import platform
from schemas import PcInfo

if platform.system() == "Windows":
    try:
        import wmi
        w = wmi.WMI(namespace="root\\wmi")
    except ImportError:
        w = None

def get_session_start():
    session_start = datetime.now()
    return session_start.strftime("%d/%m/%Y %H:%M:%S")

from pydantic import BaseModel
import psutil
import platform

if platform.system() == "Windows":
    try:
        import wmi
        w = wmi.WMI(namespace="root\\wmi")
    except ImportError:
        w = None
else:
    w = None

class PcInfo(BaseModel):
    cpu_usage: float
    ram_usage: float
    cpu_temp: float  # Temperatura média da CPU; -1.0 se não disponível

def get_pc_info() -> PcInfo:
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    ram_usage = memory.percent

    cpu_temp = -1.0  # Valor padrão

    try:
        temps = psutil.sensors_temperatures()
        # Procurar qualquer grupo de sensores com "core", "package", etc.
        candidates = [k for k in temps.keys() if k.lower() in ["coretemp", "cpu-thermal", "acpitz", "package id 0"]]

        # Se houver sensores válidos
        for key in candidates:
            entries = temps.get(key)
            if entries:
                valid_temps = [entry.current for entry in entries if entry.current is not None]
                if valid_temps:
                    cpu_temp = sum(valid_temps) / len(valid_temps)
                    break  # Para no primeiro grupo válido
    except Exception:
        pass

    # Fallback para Windows (WMI)
    if cpu_temp == -1.0 and platform.system() == "Windows" and w:
        try:
            temperature_info = w.MSAcpi_ThermalZoneTemperature()
            if temperature_info:
                temps_kelvin = [
                    (t.CurrentTemperature / 10) - 273.15
                    for t in temperature_info
                    if t.CurrentTemperature is not None
                ]
                if temps_kelvin:
                    cpu_temp = sum(temps_kelvin) / len(temps_kelvin)
        except Exception:
            pass

    return PcInfo(
        cpu_usage=cpu_usage,
        ram_usage=ram_usage,
        cpu_temp=round(cpu_temp, 1)
    )
