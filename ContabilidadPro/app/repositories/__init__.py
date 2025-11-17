"""
Módulo de repositorios - Exporta todos los repositorios de la aplicación
"""
from app.repositories.base_repository import BaseRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.cuenta_repository import CuentaRepository
from app.repositories.transaccion_repository import TransaccionRepository
from app.repositories.auditoria_repository import AuditoriaRepository

__all__ = [
    'BaseRepository',
    'UsuarioRepository',
    'CuentaRepository',
    'TransaccionRepository',
    'AuditoriaRepository'
]
