"""
Modelo base con campos comunes para todos los modelos
"""
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from app.core.database import Base


class BaseModel(Base):
    """Clase base abstracta para todos los modelos"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
