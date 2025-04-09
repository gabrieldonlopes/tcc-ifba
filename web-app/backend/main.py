import uvicorn
import argparse
import os

from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware

from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv

from backend.database import create_tables
from backend.routers import session,config

from schemas import User,MachineResponse

load_dotenv()
WEB_API_KEY = os.getenv("WEB_API_KEY")

app = FastAPI(debug=True)

origins = [
    # adicionar link do servidor npm
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(session.router, prefix="/session")
app.include_router(config.router, prefix="/config")

def verify_key(api_key:str = Header(...)):
    if api_key != WEB_API_KEY:
        raise HTTPException(status_code=401, detail="Chave de API inválida")


@app.post("/data", dependencies=[Depends(verify_key)])
def send_data(machine_response: MachineResponse):
    sessions.append(machine_response)
    return "user registered"

@app.get("/data")
def get_data():
    return sessions


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run-server",
        action="store_true",
        help="Inicia o servidor Uvicorn."
    )
    parser.add_argument(
        "--create-db",
        action="store_true",
        help="Cria o banco de dados e as tabelas necessárias."
    )
    args = parser.parse_args()

    if args.run_server:
        uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)