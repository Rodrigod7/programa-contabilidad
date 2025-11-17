"""
Servicio de Validaciones
"""
import re
from typing import Tuple


class ValidacionService:
    """Servicio para validaciones de datos"""
    
    @staticmethod
    def validar_monto(monto: float) -> Tuple[bool, str]:
        """
        Valida que un monto sea válido
        
        Args:
            monto: Monto a validar
            
        Returns:
            Tupla (es_valido, mensaje)
        """
        if not isinstance(monto, (int, float)):
            return False, "El monto debe ser un número"
        
        if monto <= 0:
            return False, "El monto debe ser mayor a cero"
        
        if monto > 999999999.99:
            return False, "El monto es demasiado grande"
        
        return True, "Monto válido"
    
    @staticmethod
    def validar_username(username: str) -> Tuple[bool, str]:
        """
        Valida un nombre de usuario
        
        Args:
            username: Username a validar
            
        Returns:
            Tupla (es_valido, mensaje)
        """
        if not username or len(username.strip()) == 0:
            return False, "El nombre de usuario no puede estar vacío"
        
        if len(username) < 3:
            return False, "El nombre de usuario debe tener al menos 3 caracteres"
        
        if len(username) > 50:
            return False, "El nombre de usuario no puede tener más de 50 caracteres"
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            return False, "El nombre de usuario solo puede contener letras, números, guiones y guiones bajos"
        
        return True, "Username válido"
    
    @staticmethod
    def validar_password(password: str, min_length: int = 6) -> Tuple[bool, str]:
        """
        Valida una contraseña
        
        Args:
            password: Contraseña a validar
            min_length: Longitud mínima requerida
            
        Returns:
            Tupla (es_valido, mensaje)
        """
        if not password:
            return False, "La contraseña no puede estar vacía"
        
        if len(password) < min_length:
            return False, f"La contraseña debe tener al menos {min_length} caracteres"
        
        if len(password) > 100:
            return False, "La contraseña es demasiado larga"
        
        return True, "Contraseña válida"
    
    @staticmethod
    def validar_documento(documento: str) -> Tuple[bool, str]:
        """
        Valida un número de documento
        
        Args:
            documento: Documento a validar
            
        Returns:
            Tupla (es_valido, mensaje)
        """
        if not documento or len(documento.strip()) == 0:
            return False, "El documento no puede estar vacío"
        
        # Permitir solo números y guiones
        if not re.match(r'^[0-9-]+$', documento):
            return False, "El documento solo puede contener números y guiones"
        
        if len(documento) < 6:
            return False, "El documento es demasiado corto"
        
        if len(documento) > 20:
            return False, "El documento es demasiado largo"
        
        return True, "Documento válido"
    
    @staticmethod
    def validar_nombre(nombre: str, campo: str = "nombre") -> Tuple[bool, str]:
        """
        Valida un nombre o apellido
        
        Args:
            nombre: Nombre a validar
            campo: Nombre del campo para el mensaje de error
            
        Returns:
            Tupla (es_valido, mensaje)
        """
        if not nombre or len(nombre.strip()) == 0:
            return False, f"El {campo} no puede estar vacío"
        
        if len(nombre) < 2:
            return False, f"El {campo} debe tener al menos 2 caracteres"
        
        if len(nombre) > 100:
            return False, f"El {campo} es demasiado largo"
        
        # Permitir letras, espacios, acentos y algunos caracteres especiales
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\'-]+$', nombre):
            return False, f"El {campo} contiene caracteres no permitidos"
        
        return True, f"{campo.capitalize()} válido"
    
    @staticmethod
    def validar_codigo_cuenta(codigo: str) -> Tuple[bool, str]:
        """
        Valida un código de cuenta
        
        Args:
            codigo: Código a validar
            
        Returns:
            Tupla (es_valido, mensaje)
        """
        if not codigo or len(codigo.strip()) == 0:
            return False, "El código no puede estar vacío"
        
        if len(codigo) < 2:
            return False, "El código es demasiado corto"
        
        if len(codigo) > 20:
            return False, "El código es demasiado largo"
        
        # Permitir letras, números y guiones
        if not re.match(r'^[A-Z0-9-]+$', codigo):
            return False, "El código solo puede contener letras mayúsculas, números y guiones"
        
        return True, "Código válido"
    
    @staticmethod
    def validar_concepto(concepto: str) -> Tuple[bool, str]:
        """
        Valida un concepto/descripción
        
        Args:
            concepto: Concepto a validar
            
        Returns:
            Tupla (es_valido, mensaje)
        """
        if not concepto or len(concepto.strip()) == 0:
            return False, "El concepto no puede estar vacío"
        
        if len(concepto) < 3:
            return False, "El concepto debe tener al menos 3 caracteres"
        
        if len(concepto) > 500:
            return False, "El concepto es demasiado largo"
        
        return True, "Concepto válido"
