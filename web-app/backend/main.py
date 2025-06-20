import uvicorn
import argparse
import asyncio
import os

from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

from database import create_tables

from routers import (
    machine_config_endpoints,lab_endpoints,user,
    session_endpoints,task_endpoints,auth
)

load_dotenv()
WEB_API_KEY = os.getenv("WEB_API_KEY")

app = FastAPI(debug=True)

origins = [
    "http://localhost:5173",
]

app.add_middleware( # serve para restringir o acesso da API
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def initialize_db(create_db: bool): # verifica se a db existe
    if create_db:
        await create_tables()
        
#TODO: melhorar essa verificacao de chave, pois ela deve ser feita via param, não header
def verify_key(api_key:str = Header(...)):
    if api_key != WEB_API_KEY:
        raise HTTPException(status_code=401, detail="Chave de API inválida")

app.include_router(user.router)
app.include_router(auth.router, prefix="/auth")
app.include_router(session_endpoints.router, prefix="/session", dependencies=[Depends(verify_key)])
app.include_router(machine_config_endpoints.router, prefix="/machine_config", dependencies=[Depends(verify_key)])     
app.include_router(lab_endpoints.router, prefix="/lab", dependencies=[Depends(verify_key)])     
app.include_router(task_endpoints.router, prefix="/tasks", dependencies=[Depends(verify_key)])

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

    if args.create_db:
        asyncio.run(initialize_db(args.create_db))

    if args.run_server:
        uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
    