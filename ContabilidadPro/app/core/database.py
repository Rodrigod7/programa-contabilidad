"""
Configuración de la base de datos
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
import config

# Crear engine
engine = create_engine(
    config.DATABASE_URL,
    echo=False,  # True para debug SQL
    connect_args={"check_same_thread": False}  # Necesario para SQLite
)

# Session factory
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Base para modelos
Base = declarative_base()

@contextmanager
def get_session():
    """Context manager para sesiones de base de datos"""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def init_db():
    """Inicializa la base de datos creando todas las tablas"""
    from app.models import base  # Importar todos los modelos
    Base.metadata.create_all(engine)

def drop_db():
    """Elimina todas las tablas (usar con precaución)"""
    Base.metadata.drop_all(engine)
