@echo off
setlocal EnableDelayedExpansion

:: ============================================================================
:: Script de Instalacao e Configuracao de Ambiente Python
:: ============================================================================

:: --- Bloco de Configuracao ---
set "PYTHON_VERSION=3.11.9"
set "PYTHON_SERIES=311"
set "PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe"
set "PYTHON_INSTALLER=python-installer.exe"
set "VENV_NAME=.venv"

:: --- Diretório de Execução ---
set "SCRIPT_DIR=%~dp0"
set "VENV_PATH=%SCRIPT_DIR%%VENV_NAME%"
set "REQUIREMENTS_FILE=%SCRIPT_DIR%requirements.txt"
set "MAIN_SCRIPT_PATH=%SCRIPT_DIR%main.py"

:: --- 1. Verificacao de Privilegios de Administrador ---
echo [INFO] Verificando privilegios de administrador...
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [AVISO] Este script precisa ser executado como Administrador.
    echo [INFO] Tentando reiniciar com privilegios elevados...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
echo [OK] Script em execucao como Administrador.
echo.

:: --- 2. Verificacao e Instalacao do Python ---
echo [INFO] Verificando se o Python esta instalado...

set "PYTHON_EXE_PATH=%ProgramFiles%\Python%PYTHON_SERIES%\python.exe"

where python >nul 2>nul
if errorlevel 1 (
    if not exist "!PYTHON_EXE_PATH!" (
        echo [AVISO] Python nao encontrado. Baixando e instalando a versao %PYTHON_VERSION%...

        echo [INFO] Baixando o instalador do Python...
        powershell -Command "Invoke-WebRequest -Uri '!PYTHON_URL!' -OutFile '!SCRIPT_DIR!!PYTHON_INSTALLER!'"

        if not exist "!SCRIPT_DIR!!PYTHON_INSTALLER!" (
            echo [ERRO] Falha ao baixar o instalador do Python.
            pause
            exit /b 1
        )

        echo [INFO] Instalando o Python...
        start /wait "" "!SCRIPT_DIR!!PYTHON_INSTALLER!" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
        del /f "!SCRIPT_DIR!!PYTHON_INSTALLER!"

        if not exist "!PYTHON_EXE_PATH!" (
            echo [ERRO] A instalacao do Python falhou.
            pause
            exit /b 1
        )
        echo [OK] Python instalado com sucesso.
    ) else (
        echo [OK] Python encontrado na pasta padrao.
    )
) else (
    echo [OK] Python ja esta no PATH.
    set "PYTHON_EXE_PATH=python"
)
echo.

:: --- 3. Criacao e Ativacao do Ambiente Virtual ---
echo [INFO] Gerenciando o ambiente virtual (!VENV_NAME!)...

if not exist "!VENV_PATH!\Scripts\activate.bat" (
    echo [INFO] Criando ambiente virtual...
    "!PYTHON_EXE_PATH!" -m venv "!VENV_PATH!"
    if errorlevel 1 (
        echo [ERRO] Falha ao criar o ambiente virtual.
        pause
        exit /b 1
    )
) else (
    echo [OK] Ambiente virtual ja existe.
)

echo [INFO] Ativando o ambiente virtual...
call "!VENV_PATH!\Scripts\activate.bat"
echo.

:: --- 4. Instalacao de Dependencias ---
echo [INFO] Instalando dependencias do requirements.txt...

if not exist "!REQUIREMENTS_FILE!" (
    echo [AVISO] Arquivo requirements.txt nao encontrado em !SCRIPT_DIR!. Pulando instalacao.
) else (
    python -m pip install --upgrade pip
    pip install -r "!REQUIREMENTS_FILE!"
    if errorlevel 1 (
        echo [ERRO] Falha ao instalar dependencias.
        pause
        exit /b 1
    )
)
echo [OK] Dependencias instaladas.
echo.

:: --- 5. Criacao do Atalho na Inicializacao ---
echo [INFO] Configurando inicializacao automatica...

set "VENV_PYTHONW_EXE=!VENV_PATH!\Scripts\pythonw.exe"
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_PATH=!STARTUP_FOLDER!\PythonApp.lnk"

powershell -ExecutionPolicy Bypass -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('!SHORTCUT_PATH!'); $s.TargetPath = '!VENV_PYTHONW_EXE!'; $s.Arguments = '\"!MAIN_SCRIPT_PATH!\"'; $s.WorkingDirectory = '!SCRIPT_DIR!'; $s.Save()"

if exist "!SHORTCUT_PATH!" (
    echo [OK] Atalho criado com sucesso.
) else (
    echo [ERRO] Falha ao criar atalho.
)
echo.

:: --- Finalizacao ---
echo [SUCESSO] Instalacao e configuracao finalizadas.
pause
exit /b 0
