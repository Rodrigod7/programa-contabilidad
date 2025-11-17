"""
Repositorio para el modelo Cuenta
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.cuenta import Cuenta
from app.repositories.base_repository import BaseRepository


class CuentaRepository(BaseRepository[Cuenta]):
    """Repositorio para operaciones con cuentas contables"""
    
    def __init__(self, session: Session):
        super().__init__(Cuenta, session)
    
    def get_by_codigo(self, codigo: str) -> Optional[Cuenta]:
        """
        Obtiene una cuenta por su código
        
        Args:
            codigo: Código de la cuenta
            
        Returns:
            Cuenta o None
        """
        return self.session.query(Cuenta).filter(
            Cuenta.codigo == codigo
        ).first()
    
    def get_by_tipo(self, tipo: str) -> List[Cuenta]:
        """
        Obtiene todas las cuentas de un tipo específico
        
        Args:
            tipo: Tipo de cuenta (Activo Corriente, Pasivo, etc.)
            
        Returns:
            Lista de cuentas del tipo especificado
        """
        return self.session.query(Cuenta).filter(
            Cuenta.tipo == tipo
        ).all()
    
    def get_activas(self) -> List[Cuenta]:
        """
        Obtiene todas las cuentas activas
        
        Returns:
            Lista de cuentas activas
        """
        return self.session.query(Cuenta).filter(
            Cuenta.activa == 1
        ).all()
    
    def get_by_naturaleza(self, naturaleza: str) -> List[Cuenta]:
        """
        Obtiene cuentas por naturaleza
        
        Args:
            naturaleza: Naturaleza de la cuenta (Deudora/Acreedora)
            
        Returns:
            Lista de cuentas con esa naturaleza
        """
        return self.session.query(Cuenta).filter(
            Cuenta.naturaleza == naturaleza
        ).all()
    
    def codigo_exists(self, codigo: str) -> bool:
        """
        Verifica si existe un código de cuenta
        
        Args:
            codigo: Código a verificar
            
        Returns:
            True si existe, False en caso contrario
        """
        return self.session.query(Cuenta).filter(
            Cuenta.codigo == codigo
        ).count() > 0
    
    def actualizar_saldo(self, cuenta_id: int, nuevo_saldo: float) -> Optional[Cuenta]:
        """
        Actualiza el saldo de una cuenta
        
        Args:
            cuenta_id: ID de la cuenta
            nuevo_saldo: Nuevo saldo de la cuenta
            
        Returns:
            Cuenta actualizada o None
        """
        return self.update(cuenta_id, saldo=nuevo_saldo)
    
    def sumar_al_saldo(self, cuenta_id: int, monto: float) -> Optional[Cuenta]:
        """
        Suma un monto al saldo actual de la cuenta
        
        Args:
            cuenta_id: ID de la cuenta
            monto: Monto a sumar (puede ser negativo)
            
        Returns:
            Cuenta actualizada o None
        """
        cuenta = self.get_by_id(cuenta_id)
        if cuenta:
            cuenta.saldo += monto
            self.session.flush()
        return cuenta
