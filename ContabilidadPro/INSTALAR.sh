#!/bin/bash

echo "========================================"
echo " ContabilidadPro - Instalación Rápida"
echo "========================================"
echo ""

# Verificar que Python esté instalado
if ! command -v python3 &> /dev/null
then
    echo "ERROR: Python 3 no está instalado"
    echo "Por favor instale Python 3.10 o superior"
    exit 1
fi

echo "[1/4] Python detectado"
python3 --version

echo ""
echo "[2/4] Creando entorno virtual..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudo crear el entorno virtual"
    exit 1
fi

echo ""
echo "[3/4] Activando entorno virtual..."
source venv/bin/activate

echo ""
echo "[4/4] Instalando dependencias..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudieron instalar las dependencias"
    exit 1
fi

echo ""
echo "========================================"
echo " Instalación completada exitosamente!"
echo "========================================"
echo ""
echo "Para ejecutar la aplicación:"
echo "  1. Activa el entorno: source venv/bin/activate"
echo "  2. Ejecuta: python main.py"
echo ""
echo "O simplemente ejecuta: ./EJECUTAR.sh"
echo ""
