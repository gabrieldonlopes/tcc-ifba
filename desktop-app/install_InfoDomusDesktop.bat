@echo off
setlocal

echo [INFO] Criando ambiente virtual...
python -m venv .venv

echo [INFO] Ativando ambiente virtual...
call .venv\Scripts\activate.bat

echo [INFO] Instalando dependências...
pip install --upgrade pip
pip install -r requirements.txt

echo [INFO] Criando tarefa agendada para iniciar o aplicativo com o Windows...

:: Define caminho completo do main.py
set "TASK_PATH=%~dp0main.py"

:: Criar a tarefa agendada (executa sem argumentos)
schtasks /create /tn "InfoDomusDesktop" ^
  /tr "\"%~dp0.venv\Scripts\python.exe\" \"%TASK_PATH%\"" ^
  /sc onlogon /rl HIGHEST /f

echo [OK] Instalação completa e tarefa criada.
pause
