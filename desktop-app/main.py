import argparse
from  views.ComputerAccess import ComputerAccess


app = ComputerAccess()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run-app",
        action="store_true",
        help="Inicia aplicacao Desktop."
    )
    args = parser.parse_args()

    if args.run_app:
        app.render()
