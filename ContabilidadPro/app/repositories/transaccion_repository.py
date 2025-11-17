"""
Repositorio para el modelo Transacción
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from app.models.transaccion import Transaccion
from app.repositories.base_repository import BaseRepository


class TransaccionRepository(BaseRepository[Transaccion]):
    """Repositorio para operaciones con transacciones"""
    
    def __init__(self, session: Session):
        super().__init__(Transaccion, session)
    
    def get_by_cuenta(self, cuenta_id: int) -> List[Transaccion]:
        """
        Obtiene todas las transacciones de una cuenta
        
        Args:
            cuenta_id: ID de la cuenta
            
        Returns:
            Lista de transacciones
        """
        return self.session.query(Transaccion).filter(
            Transaccion.cuenta_id == cuenta_id
        ).order_by(Transaccion.fecha.desc()).all()
    
    def get_by_periodo(self, periodo_id: int) -> List[Transaccion]:
        """
        Obtiene todas las transacciones de un período
        
        Args:
            periodo_id: ID del período
            
        Returns:
            Lista de transacciones
        """
        return self.session.query(Transaccion).filter(
            Transaccion.periodo_id == periodo_id
        ).order_by(Transaccion.fecha.desc()).all()
    
    def get_by_tipo(self, tipo: str) -> List[Transaccion]:
        """
        Obtiene transacciones por tipo
        
        Args:
            tipo: Tipo de transacción (Venta, Compra, General)
            
        Returns:
            Lista de transacciones
        """
        return self.session.query(Transaccion).filter(
            Transaccion.tipo == tipo
        ).order_by(Transaccion.fecha.desc()).all()
    
    def get_by_fecha_rango(self, fecha_inicio: datetime, fecha_fin: datetime) -> List[Transaccion]:
        """
        Obtiene transacciones en un rango de fechas
        
        Args:
            fecha_inicio: Fecha inicial
            fecha_fin: Fecha final
            
        Returns:
            Lista de transacciones
        """
        return self.session.query(Transaccion).filter(
            and_(
                Transaccion.fecha >= fecha_inicio,
                Transaccion.fecha <= fecha_fin
            )
        ).order_by(Transaccion.fecha.desc()).all()
    
    def get_by_usuario(self, usuario_id: int) -> List[Transaccion]:
        """
        Obtiene transacciones realizadas por un usuario
        
        Args:
            usuario_id: ID del usuario
            
        Returns:
            Lista de transacciones
        """
        return self.session.query(Transaccion).filter(
            Transaccion.usuario_id == usuario_id
        ).order_by(Transaccion.fecha.desc()).all()
    
    def get_total_por_tipo(self, tipo: str, periodo_id: Optional[int] = None) -> float:
        """
        Calcula el total de transacciones por tipo
        
        Args:
            tipo: Tipo de transacción
            periodo_id: ID del período (opcional)
            
        Returns:
            Total de montos
        """
        query = self.session.query(func.sum(Transaccion.monto)).filter(
            Transaccion.tipo == tipo
        )
        
        if periodo_id:
            query = query.filter(Transaccion.periodo_id == periodo_id)
        
        result = query.scalar()
        return result if result else 0.0
    
    def buscar(self, termino: str) -> List[Transaccion]:
        """
        Busca transacciones por término en el concepto
        
        Args:
            termino: Término a buscar
            
        Returns:
            Lista de transacciones que coinciden
        """
        return self.session.query(Transaccion).filter(
            Transaccion.concepto.like(f'%{termino}%')
        ).order_by(Transaccion.fecha.desc()).all()
