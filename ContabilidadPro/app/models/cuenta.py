"""
Modelo de Cuenta Contable
"""
from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.core.constants import NATURALEZA_DEUDORA, NATURALEZA_ACREEDORA


class Cuenta(BaseModel):
    """Modelo de cuenta contable"""
    __tablename__ = 'cuentas'
    
    codigo = Column(String(20), unique=True, nullable=False, index=True)
    nombre = Column(String(200), nullable=False)
    tipo = Column(String(50), nullable=False)  # Activo Corriente, Pasivo, etc.
    naturaleza = Column(String(20), nullable=False)  # Deudora o Acreedora
    saldo = Column(Float, default=0.0, nullable=False)
    activa = Column(Integer, default=1)  # 1 = activa, 0 = inactiva
    
    # Relaciones
    transacciones = relationship("Transaccion", back_populates="cuenta", cascade="all, delete-orphan")
    
    @property
    def es_deudora(self):
        """Verifica si la cuenta tiene naturaleza deudora"""
        return self.naturaleza == NATURALEZA_DEUDORA
    
    @property
    def es_acreedora(self):
        """Verifica si la cuenta tiene naturaleza acreedora"""
        return self.naturaleza == NATURALEZA_ACREEDORA
    
    def __repr__(self):
        return f"<Cuenta(codigo='{self.codigo}', nombre='{self.nombre}', saldo={self.saldo})>"
