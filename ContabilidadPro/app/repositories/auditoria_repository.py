"""
Repositorio para el modelo Auditoría
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.auditoria import Auditoria
from app.repositories.base_repository import BaseRepository


class AuditoriaRepository(BaseRepository[Auditoria]):
    """Repositorio para operaciones con auditoría"""
    
    def __init__(self, session: Session):
        super().__init__(Auditoria, session)
    
    def get_by_usuario(self, usuario_id: int) -> List[Auditoria]:
        """
        Obtiene todas las actividades de un usuario
        
        Args:
            usuario_id: ID del usuario
            
        Returns:
            Lista de actividades del usuario
        """
        return self.session.query(Auditoria).filter(
            Auditoria.usuario_id == usuario_id
        ).order_by(Auditoria.fecha_hora.desc()).all()
    
    def get_by_tipo(self, tipo_actividad: str) -> List[Auditoria]:
        """
        Obtiene actividades por tipo
        
        Args:
            tipo_actividad: Tipo de actividad
            
        Returns:
            Lista de actividades del tipo especificado
        """
        return self.session.query(Auditoria).filter(
            Auditoria.tipo_actividad == tipo_actividad
        ).order_by(Auditoria.fecha_hora.desc()).all()
    
    def get_by_fecha_rango(self, fecha_inicio: datetime, fecha_fin: datetime) -> List[Auditoria]:
        """
        Obtiene actividades en un rango de fechas
        
        Args:
            fecha_inicio: Fecha inicial
            fecha_fin: Fecha final
            
        Returns:
            Lista de actividades
        """
        return self.session.query(Auditoria).filter(
            and_(
                Auditoria.fecha_hora >= fecha_inicio,
                Auditoria.fecha_hora <= fecha_fin
            )
        ).order_by(Auditoria.fecha_hora.desc()).all()
    
    def get_recientes(self, limite: int = 100) -> List[Auditoria]:
        """
        Obtiene las actividades más recientes
        
        Args:
            limite: Número máximo de actividades a retornar
            
        Returns:
            Lista de actividades recientes
        """
        return self.session.query(Auditoria).order_by(
            Auditoria.fecha_hora.desc()
        ).limit(limite).all()
    
    def registrar_actividad(self, usuario_id: int, tipo_actividad: str, 
                           descripcion: str, ip_address: Optional[str] = None) -> Auditoria:
        """
        Registra una nueva actividad
        
        Args:
            usuario_id: ID del usuario
            tipo_actividad: Tipo de actividad
            descripcion: Descripción de la actividad
            ip_address: Dirección IP (opcional)
            
        Returns:
            Registro de auditoría creado
        """
        return self.create(
            usuario_id=usuario_id,
            tipo_actividad=tipo_actividad,
            descripcion=descripcion,
            ip_address=ip_address,
            fecha_hora=datetime.now()
        )
    
    def buscar(self, termino: str) -> List[Auditoria]:
        """
        Busca en las descripciones de actividades
        
        Args:
            termino: Término a buscar
            
        Returns:
            Lista de actividades que coinciden
        """
        return self.session.query(Auditoria).filter(
            Auditoria.descripcion.like(f'%{termino}%')
        ).order_by(Auditoria.fecha_hora.desc()).all()
