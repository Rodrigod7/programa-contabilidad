"""
Modelo de Período Contable
"""
from sqlalchemy import Column, String, DateTime, Integer, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import BaseModel


class Periodo(BaseModel):
    """Modelo de período contable"""
    __tablename__ = 'periodos'
    
    nombre = Column(String(100), nullable=False)  # Ej: "Enero 2024", "2024"
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=True)  # Null si el período está abierto
    cerrado = Column(Integer, default=0)  # 0 = abierto, 1 = cerrado
    resultado = Column(Float, default=0.0)  # Resultado del período al cerrarlo
    
    # Relaciones
    asientos = relationship("Asiento", back_populates="periodo", cascade="all, delete-orphan")
    transacciones = relationship("Transaccion", back_populates="periodo", cascade="all, delete-orphan")
    
    @property
    def esta_abierto(self):
        """Verifica si el período está abierto"""
        return self.cerrado == 0
    
    @property
    def esta_cerrado(self):
        """Verifica si el período está cerrado"""
        return self.cerrado == 1
    
    def __repr__(self):
        estado = "Cerrado" if self.esta_cerrado else "Abierto"
        return f"<Periodo(nombre='{self.nombre}', estado='{estado}')>"
