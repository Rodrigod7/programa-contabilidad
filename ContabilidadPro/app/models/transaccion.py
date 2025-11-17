"""
Modelo de Transacción Contable
"""
from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import BaseModel


class Transaccion(BaseModel):
    """Modelo de transacción contable"""
    __tablename__ = 'transacciones'
    
    fecha = Column(DateTime, default=datetime.now, nullable=False)
    concepto = Column(String(500), nullable=False)
    monto = Column(Float, nullable=False)
    tipo = Column(String(50), nullable=False)  # Venta, Compra, General
    
    # Foreign Keys
    cuenta_id = Column(Integer, ForeignKey('cuentas.id'), nullable=False)
    asiento_id = Column(Integer, ForeignKey('asientos.id'), nullable=True)
    periodo_id = Column(Integer, ForeignKey('periodos.id'), nullable=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    
    # Relaciones
    cuenta = relationship("Cuenta", back_populates="transacciones")
    asiento = relationship("Asiento", back_populates="transacciones")
    periodo = relationship("Periodo", back_populates="transacciones")
    usuario = relationship("Usuario")
    
    def __repr__(self):
        return f"<Transaccion(fecha='{self.fecha}', concepto='{self.concepto}', monto={self.monto})>"
