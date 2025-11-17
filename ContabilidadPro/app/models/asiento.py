"""
Modelo de Asiento Contable
"""
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import BaseModel


class Asiento(BaseModel):
    """Modelo de asiento contable (partida doble)"""
    __tablename__ = 'asientos'
    
    fecha = Column(DateTime, default=datetime.now, nullable=False)
    descripcion = Column(String(500), nullable=False)
    numero = Column(Integer, nullable=False, unique=True)  # Número consecutivo de asiento
    
    # Foreign Keys
    periodo_id = Column(Integer, ForeignKey('periodos.id'), nullable=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    
    # Relaciones
    transacciones = relationship("Transaccion", back_populates="asiento", cascade="all, delete-orphan")
    periodo = relationship("Periodo", back_populates="asientos")
    usuario = relationship("Usuario")
    
    @property
    def total_debe(self):
        """Calcula el total del debe"""
        return sum(t.monto for t in self.transacciones if t.cuenta.es_deudora)
    
    @property
    def total_haber(self):
        """Calcula el total del haber"""
        return sum(t.monto for t in self.transacciones if t.cuenta.es_acreedora)
    
    @property
    def esta_balanceado(self):
        """Verifica si el asiento está balanceado (debe = haber)"""
        return abs(self.total_debe - self.total_haber) < 0.01
    
    def __repr__(self):
        return f"<Asiento(numero={self.numero}, fecha='{self.fecha}', descripcion='{self.descripcion}')>"
