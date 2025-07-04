@echo off
setlocal

echo [INFO] Removendo tarefa agendada...
schtasks /delete /tn "InfoDomusDesktop" /f

echo [INFO] Apagando ambiente virtual...
rmdir /s /q .venv

echo [OK] Processo desfeito.
pause
