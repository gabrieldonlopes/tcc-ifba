@echo off
setlocal

:: ============================================================================
:: Script de Inicialização da Aplicação
::
:: Este script ativa o ambiente virtual e executa o main.py.
:: Deve ser colocado na mesma pasta que o diretório .venv e main.py.
:: ============================================================================

echo [INFO] Ativando o ambiente virtual...

:: Define o caminho para o script de ativação
set "VENV_ACTIVATE_SCRIPT=%~dp0.venv\Scripts\activate.bat"

:: Verifica se o ambiente virtual existe
if not exist "%VENV_ACTIVATE_SCRIPT%" (
    echo [ERRO] Ambiente virtual nao encontrado!
    echo [INFO] Por favor, execute o script 'install.bat' primeiro.
    pause
    exit /b 1
)

:: Ativa o ambiente virtual
call "%VENV_ACTIVATE_SCRIPT%"

echo [INFO] Iniciando a aplicacao (main.py)...
echo.

:: Executa o script Python
:: Usamos "python" aqui, pois o ambiente virtual já está ativado e no PATH
python "%~dp0main.py"

echo.
echo [INFO] A aplicacao foi fechada. Pressione qualquer tecla para sair.
pause >nul
