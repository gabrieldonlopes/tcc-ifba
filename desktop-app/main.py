import argparse
from  views.ComputerAccessTemplate import ComputerAccessTemplate
from views.ConfigMachineTemplate import ConfigMachineTemplate 
from config import get_local_config

local_config = get_local_config()

if local_config:
    app = ComputerAccessTemplate(machine_name=local_config.machine_name,classes=local_config.classes,lab_name=local_config.lab_name)
else:
    app = ConfigMachineTemplate()
    
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
