@echo off
setlocal EnableDelayedExpansion

:: ============================================================================
:: Script de Desinstalação (Otimizado)
::
:: Remove o atalho direto da pasta de Inicialização e o ambiente virtual.
:: ============================================================================

:: --- Bloco de Configuração ---
set "VENV_NAME=.venv"
set "APP_NAME=InfoDomusDesktop"

:: --- 1. Remoção do Atalho da Inicialização ---
echo [INFO] Removendo atalho da inicializacao...
set "SHORTCUT_PATH=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\!APP_NAME!.lnk"

if exist "!SHORTCUT_PATH!" (
    del /f "!SHORTCUT_PATH!"
    echo [OK] Atalho de inicializacao removido.
) else (
    echo [AVISO] Atalho de inicializacao nao encontrado.
)
echo.

:: --- 2. Remoção de arquivos auxiliares antigos (limpeza) ---
echo [INFO] Removendo arquivos auxiliares de versoes antigas...
if exist "%~dp0start_hidden.vbs" (
    del /f "%~dp0start_hidden.vbs"
)

:: --- 3. Remoção do Ambiente Virtual ---
echo [INFO] Removendo o ambiente virtual (!VENV_NAME!)...
if exist "%VENV_NAME%" (
    rmdir /s /q "%VENV_NAME%"
    echo [OK] Ambiente virtual removido.
) else (
    echo [AVISO] O diretorio do ambiente virtual nao foi encontrado.
)
echo.

:: --- Finalização ---
echo [SUCESSO] Processo de desinstalacao concluido.
pause
exit /b 0