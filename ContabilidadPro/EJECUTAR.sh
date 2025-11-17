#!/bin/bash

echo "========================================"
echo " Iniciando ContabilidadPro..."
echo "========================================"
echo ""

# Verificar si existe el entorno virtual
if [ ! -f "venv/bin/activate" ]; then
    echo "ERROR: Entorno virtual no encontrado"
    echo "Por favor ejecuta ./INSTALAR.sh primero"
    exit 1
fi

# Activar entorno virtual
source venv/bin/activate

# Ejecutar aplicación
python main.py

# Desactivar entorno virtual al cerrar
deactivate
