"""
Repositorio para el modelo Usuario
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.repositories.base_repository import BaseRepository


class UsuarioRepository(BaseRepository[Usuario]):
    """Repositorio para operaciones con usuarios"""
    
    def __init__(self, session: Session):
        super().__init__(Usuario, session)
    
    def get_by_username(self, username: str) -> Optional[Usuario]:
        """
        Obtiene un usuario por su username
        
        Args:
            username: Nombre de usuario
            
        Returns:
            Usuario o None
        """
        return self.session.query(Usuario).filter(
            Usuario.username == username
        ).first()
    
    def get_by_documento(self, documento: str) -> Optional[Usuario]:
        """
        Obtiene un usuario por su documento
        
        Args:
            documento: Número de documento
            
        Returns:
            Usuario o None
        """
        return self.session.query(Usuario).filter(
            Usuario.documento == documento
        ).first()
    
    def username_exists(self, username: str) -> bool:
        """
        Verifica si existe un username
        
        Args:
            username: Nombre de usuario
            
        Returns:
            True si existe, False en caso contrario
        """
        return self.session.query(Usuario).filter(
            Usuario.username == username
        ).count() > 0
    
    def documento_exists(self, documento: str) -> bool:
        """
        Verifica si existe un documento
        
        Args:
            documento: Número de documento
            
        Returns:
            True si existe, False en caso contrario
        """
        return self.session.query(Usuario).filter(
            Usuario.documento == documento
        ).count() > 0
    
    def get_activos(self):
        """
        Obtiene todos los usuarios activos
        
        Returns:
            Lista de usuarios activos
        """
        return self.session.query(Usuario).filter(
            Usuario.activo == 1
        ).all()
    
    def get_by_nivel(self, nivel: int):
        """
        Obtiene usuarios por nivel
        
        Args:
            nivel: Nivel de usuario (1=Trabajador, 2=Administrador)
            
        Returns:
            Lista de usuarios del nivel especificado
        """
        return self.session.query(Usuario).filter(
            Usuario.nivel == nivel
        ).all()
