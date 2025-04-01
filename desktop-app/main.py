import argparse
from  views.ComputerAccessTemplate import ComputerAccessTemplate


app = ComputerAccessTemplate()

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
