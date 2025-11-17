"""
Modelo de Auditoría (Log de Actividades)
"""
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import BaseModel


class Auditoria(BaseModel):
    """Modelo de auditoría para registrar actividades del sistema"""
    __tablename__ = 'auditoria'
    
    tipo_actividad = Column(String(50), nullable=False)  # Login, Logout, Crear, etc.
    descripcion = Column(String(500), nullable=False)
    fecha_hora = Column(DateTime, default=datetime.now, nullable=False)
    ip_address = Column(String(45), nullable=True)  # Para futuras mejoras
    
    # Foreign Keys
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="actividades")
    
    def __repr__(self):
        return f"<Auditoria(tipo='{self.tipo_actividad}', usuario_id={self.usuario_id}, fecha='{self.fecha_hora}')>"
