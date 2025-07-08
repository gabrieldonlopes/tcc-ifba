import argparse
from  views.ComputerAccessTemplate import ComputerAccessTemplate
from views.ConfigMachineTemplate import ConfigMachineTemplate 
from config import get_local_config

local_config = get_local_config()

if local_config:
    app = ComputerAccessTemplate(machine_name=local_config.machine_name,classes=local_config.classes,lab_name=local_config.lab_name)
else:
    app = ConfigMachineTemplate()
    

#NOTE: pensar numa forma de armazenar dados localmente para caso o sistema não tenha acesso a internet
  

if __name__ == "__main__":
    app.run()
