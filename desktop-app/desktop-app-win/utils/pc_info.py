import os
import shutil
import platform
import psutil
from datetime import datetime

from schemas import PcInfo  # mantém seu modelo existente
# Verificação de plataforma
SYSTEM = platform.system()

# Inicialização do WMI se for Windows
w = None
if SYSTEM == "Windows":
    try:
        import wmi
        w = wmi.WMI(namespace="root\\wmi")
    except ImportError:
        pass


def get_session_start() -> str:
    """Retorna a data/hora atual formatada."""
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def get_cpu_temp() -> float:
    """Retorna a temperatura média da CPU, se possível."""
    cpu_temp = -1.0  # padrão em caso de falha

    try:
        temps = psutil.sensors_temperatures()
        candidates = [k for k in temps if k.lower() in ["coretemp", "cpu-thermal", "acpitz", "package id 0"]]

        for key in candidates:
            entries = temps[key]
            valid = [entry.current for entry in entries if entry.current is not None]
            if valid:
                return round(sum(valid) / len(valid), 1)
    except Exception:
        pass

    # Fallback WMI para Windows
    if SYSTEM == "Windows" and w:
        try:
            temps_kelvin = [
                (t.CurrentTemperature / 10) - 273.15
                for t in w.MSAcpi_ThermalZoneTemperature()
                if t.CurrentTemperature is not None
            ]
            if temps_kelvin:
                return round(sum(temps_kelvin) / len(temps_kelvin), 1)
        except Exception:
            pass

    return cpu_temp


def get_pc_info() -> PcInfo:
    """Retorna informações dinâmicas do sistema (uso e temperatura)."""
    return PcInfo(
        cpu_usage=psutil.cpu_percent(interval=1),
        ram_usage=psutil.virtual_memory().percent,
        cpu_temp=get_cpu_temp()
    )

def get_machine_config() -> dict:
    """Retorna informações estáticas do sistema (armazenamento, RAM, placa-mãe)."""
    import math
    total, _, free = shutil.disk_usage(os.path.abspath("/"))

    total_ram_gb = math.ceil(psutil.virtual_memory().total / (1024 ** 3))
    total_storage_gb = math.ceil(total / (1024 ** 3))

    manufacturer = None
    model = None

    if SYSTEM == "Windows":
        try:
            import wmi
            w = wmi.WMI()
            for board in w.Win32_BaseBoard():
                manufacturer = board.Manufacturer
                model = board.Product
                break
        except ImportError:
            print("Modulo wmi nao esta instalado. Instale com 'pip install wmi'")
        except Exception as e:
            print(f"Erro ao obter info da placa-mãe: {e}")

    elif SYSTEM == "Linux":
        try:
            with open("/sys/devices/virtual/dmi/id/board_vendor") as f:
                manufacturer = f.read().strip()
            with open("/sys/devices/virtual/dmi/id/board_name") as f:
                model = f.read().strip()
        except Exception:
            pass

    return {
        "storage": f"{total_storage_gb}GB",
        "memory": f"{total_ram_gb}GB",
        "motherboard": f"{manufacturer} {model}" if manufacturer and model else None,
    }