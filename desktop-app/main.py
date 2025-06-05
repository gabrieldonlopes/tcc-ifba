import argparse
from  views.ComputerAccessTemplate import ComputerAccessTemplate
from views.ConfigMachineTemplate import ConfigMachineTemplate 
from config import get_local_config

local_config = get_local_config()

if local_config:
    app = ComputerAccessTemplate(machine_name=local_config.machine_name,classes=local_config.classes,lab_name=local_config.lab_name)
else:
    app = ConfigMachineTemplate()
    

#TODO: resolver bug de janela
#NOTE: para facilitar o registro de máquina dados motherboard, memory etc. poderiam ser pegos automaticamente através de utils
#NOTE: o template de configuracao e suas respectivas foi retrabalhado para uso síncrono. a antiga abordagem apresentava problemas de
# desempenho em algumas máquinas
#NOTE: pensar numa forma de armazenar dados localmente para caso o sistema não tenha acesso a internet
  
#TODO: implementar métodos de visualização das sessões localmente
#TODO: implementar verificacao de senha e turma no acesso de máquina

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run-app",
        action="store_true",
        help="Inicia aplicacao Desktop."
    )
    args = parser.parse_args()

    if args.run_app:
        app.run()
