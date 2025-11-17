@echo off
echo ========================================
echo  ContabilidadPro - Instalacion Rapida
echo ========================================
echo.

REM Verificar que Python este instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado
    echo Por favor instale Python 3.10 o superior desde python.org
    pause
    exit /b 1
)

echo [1/4] Python detectado
python --version

echo.
echo [2/4] Creando entorno virtual...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: No se pudo crear el entorno virtual
    pause
    exit /b 1
)

echo.
echo [3/4] Activando entorno virtual...
call venv\Scripts\activate.bat

echo.
echo [4/4] Instalando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Instalacion completada exitosamente!
echo ========================================
echo.
echo Para ejecutar la aplicacion:
echo   1. Activa el entorno: venv\Scripts\activate
echo   2. Ejecuta: python main.py
echo.
echo O simplemente ejecuta: EJECUTAR.bat
echo.
pause
