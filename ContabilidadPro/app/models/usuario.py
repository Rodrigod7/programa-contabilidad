"""
Modelo de Usuario
"""
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.core.constants import NIVEL_ADMINISTRADOR, NIVEL_TRABAJADOR


class Usuario(BaseModel):
    """Modelo de usuario del sistema"""
    __tablename__ = 'usuarios'
    
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    documento = Column(String(20), unique=True, nullable=False)
    nivel = Column(Integer, nullable=False, default=NIVEL_TRABAJADOR)
    activo = Column(Integer, default=1)  # 1 = activo, 0 = inactivo
    
    # Relaciones
    actividades = relationship("Auditoria", back_populates="usuario", cascade="all, delete-orphan")
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del usuario"""
        return f"{self.nombre} {self.apellido}"
    
    @property
    def es_administrador(self):
        """Verifica si el usuario es administrador"""
        return self.nivel == NIVEL_ADMINISTRADOR
    
    def __repr__(self):
        return f"<Usuario(username='{self.username}', nombre='{self.nombre_completo}')>"
