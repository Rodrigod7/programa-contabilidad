"""
Repositorio base con operaciones CRUD genéricas
"""
from typing import TypeVar, Generic, Type, Optional, List
from sqlalchemy.orm import Session
from app.models.base import BaseModel

T = TypeVar('T', bound=BaseModel)


class BaseRepository(Generic[T]):
    """Repositorio base genérico con operaciones CRUD"""
    
    def __init__(self, model: Type[T], session: Session):
        """
        Inicializa el repositorio
        
        Args:
            model: Clase del modelo SQLAlchemy
            session: Sesión de base de datos
        """
        self.model = model
        self.session = session
    
    def create(self, **kwargs) -> T:
        """
        Crea un nuevo registro
        
        Args:
            **kwargs: Campos del modelo
            
        Returns:
            Instancia del modelo creado
        """
        instance = self.model(**kwargs)
        self.session.add(instance)
        self.session.flush()
        return instance
    
    def get_by_id(self, id: int) -> Optional[T]:
        """
        Obtiene un registro por ID
        
        Args:
            id: ID del registro
            
        Returns:
            Instancia del modelo o None
        """
        return self.session.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self) -> List[T]:
        """
        Obtiene todos los registros
        
        Returns:
            Lista de instancias del modelo
        """
        return self.session.query(self.model).all()
    
    def update(self, id: int, **kwargs) -> Optional[T]:
        """
        Actualiza un registro
        
        Args:
            id: ID del registro
            **kwargs: Campos a actualizar
            
        Returns:
            Instancia actualizada o None
        """
        instance = self.get_by_id(id)
        if instance:
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            self.session.flush()
        return instance
    
    def delete(self, id: int) -> bool:
        """
        Elimina un registro
        
        Args:
            id: ID del registro
            
        Returns:
            True si se eliminó, False si no existía
        """
        instance = self.get_by_id(id)
        if instance:
            self.session.delete(instance)
            self.session.flush()
            return True
        return False
    
    def count(self) -> int:
        """
        Cuenta los registros totales
        
        Returns:
            Número de registros
        """
        return self.session.query(self.model).count()
    
    def exists(self, id: int) -> bool:
        """
        Verifica si existe un registro con el ID dado
        
        Args:
            id: ID del registro
            
        Returns:
            True si existe, False en caso contrario
        """
        return self.session.query(self.model).filter(self.model.id == id).count() > 0
