"""
Configuración global de la aplicación
"""
import os
from pathlib import Path

# Rutas base
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
EXPORTS_DIR = BASE_DIR / "exports"
LOGS_DIR = BASE_DIR / "logs"
RESOURCES_DIR = BASE_DIR / "resources"

# Crear directorios si no existen
for directory in [DATA_DIR, EXPORTS_DIR, LOGS_DIR, EXPORTS_DIR / "pdf", EXPORTS_DIR / "excel", DATA_DIR / "backups"]:
    directory.mkdir(parents=True, exist_ok=True)

# Base de datos
DATABASE_URL = f"sqlite:///{DATA_DIR / 'database.db'}"

# Seguridad
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
PASSWORD_MIN_LENGTH = 6

# Aplicación
APP_NAME = "ContabilidadPro"
APP_VERSION = "1.0.0"

# Logging
LOG_FILE = LOGS_DIR / "app.log"
LOG_LEVEL = "INFO"

# Usuario Admin por defecto
DEFAULT_ADMIN = {
    'username': 'Ivan',
    'password': 'Rodri2008',
    'nombre': 'Ricardo Ivan',
    'apellido': 'Espinoza',
    'documento': '20452423',
    'nivel': 2  # 2 = Administrador, 1 = Trabajador
}
