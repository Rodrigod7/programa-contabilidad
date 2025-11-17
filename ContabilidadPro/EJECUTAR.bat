@echo off
echo ========================================
echo  Iniciando ContabilidadPro...
echo ========================================
echo.

REM Verificar si existe el entorno virtual
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Entorno virtual no encontrado
    echo Por favor ejecuta INSTALAR.bat primero
    pause
    exit /b 1
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Ejecutar aplicación
python main.py

REM Desactivar entorno virtual al cerrar
deactivate
