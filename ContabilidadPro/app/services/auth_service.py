"""
Servicio de Autenticación
"""
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.auditoria_repository import AuditoriaRepository
from app.core.security import hash_password, verify_password
from app.core.constants import ACTIVIDAD_LOGIN, ACTIVIDAD_LOGOUT, ACTIVIDAD_CREAR_USUARIO
import config


class AuthService:
    """Servicio para manejo de autenticación y usuarios"""
    
    def __init__(self, session: Session):
        self.session = session
        self.usuario_repo = UsuarioRepository(session)
        self.auditoria_repo = AuditoriaRepository(session)
        self.usuario_actual: Optional[Usuario] = None
    
    def autenticar(self, username: str, password: str) -> Tuple[bool, str, Optional[Usuario]]:
        """
        Autentica un usuario
        """
        usuario = self.usuario_repo.get_by_username(username)
        
        if not usuario:
            return False, "Usuario no encontrado", None
        
        if not usuario.activo:
            return False, "Usuario inactivo", None
        
        if not verify_password(password, usuario.password_hash):
            return False, "Contraseña incorrecta", None
        
        # Registrar login
        self.usuario_actual = usuario
        self.auditoria_repo.registrar_actividad(
            usuario_id=usuario.id,
            tipo_actividad=ACTIVIDAD_LOGIN,
            descripcion=f"Inicio de sesión: {username}"
        )
        
        # --- INICIO DE LA CORRECCIÓN ---
        
        # 1. (Opcional pero recomendado)
        #    Forzamos la carga de los atributos que usaremos 
        #    fuera de esta sesión.
        _ = usuario.username
        _ = usuario.nombre_completo
        _ = usuario.es_administrador
        
        # 2. (LA SOLUCIÓN REAL)
        #    "Expulsamos" el objeto de la sesión.
        #    Esto lo convierte en un objeto simple de Python
        #    y evita el error DetachedInstanceError.
        self.session.expunge(usuario)
        
        # --- FIN DE LA CORRECCIÓN ---
        
        # Nota: El 'self.session.commit()' se quitó en el paso anterior,
        # lo cual es correcto. El `with get_session()` en 
        # login_view.py se encargará del commit.
        
        return True, "Autenticación exitosa", usuario
    
    # ... (El resto del archivo 'auth_service.py' queda igual que en mi respuesta anterior) ...
    # (Asegúrate de que los otros métodos como cerrar_sesion,
    # crear_usuario, etc., tampoco tengan 'self.session.commit()')

    def cerrar_sesion(self):
        """Cierra la sesión del usuario actual"""
        if self.usuario_actual:
            self.auditoria_repo.registrar_actividad(
                usuario_id=self.usuario_actual.id,
                tipo_actividad=ACTIVIDAD_LOGOUT,
                descripcion=f"Cierre de sesión: {self.usuario_actual.username}"
            )
            # self.session.commit() # <--- Correcto que esté quitado
            self.usuario_actual = None
    
    def crear_usuario(self, username: str, password: str, nombre: str, 
                     apellido: str, documento: str, nivel: int) -> Tuple[bool, str]:
        """
        Crea un nuevo usuario
        """
        # Validaciones
        if not username or not password or not nombre or not apellido or not documento:
            return False, "Todos los campos son obligatorios"
        
        if len(password) < config.PASSWORD_MIN_LENGTH:
            return False, f"La contraseña debe tener al menos {config.PASSWORD_MIN_LENGTH} caracteres"
        
        if self.usuario_repo.username_exists(username):
            return False, "El nombre de usuario ya existe"
        
        if self.usuario_repo.documento_exists(documento):
            return False, "El documento ya está registrado"
        
        # Hashear contraseña
        password_hash = hash_password(password)
        
        # Crear usuario
        nuevo_usuario = self.usuario_repo.create(
            username=username,
            password_hash=password_hash,
            nombre=nombre,
            apellido=apellido,
            documento=documento,
            nivel=nivel,
            activo=1
        )
        
        # Registrar actividad
        if self.usuario_actual:
            self.auditoria_repo.registrar_actividad(
                usuario_id=self.usuario_actual.id,
                tipo_actividad=ACTIVIDAD_CREAR_USUARIO,
                descripcion=f"Usuario creado: {username} ({nombre} {apellido})"
            )
        
        # self.session.commit() # <--- Correcto que esté quitado
        return True, "Usuario creado exitosamente"
    
    def crear_admin_default(self) -> Usuario:
        """
        Crea el usuario administrador por defecto si no existe
        """
        admin_config = config.DEFAULT_ADMIN
        
        # Verificar si ya existe
        admin = self.usuario_repo.get_by_username(admin_config['username'])
        if admin:
            return admin
        
        # Crear admin
        password_hash = hash_password(admin_config['password'])
        admin = self.usuario_repo.create(
            username=admin_config['username'],
            password_hash=password_hash,
            nombre=admin_config['nombre'],
            apellido=admin_config['apellido'],
            documento=admin_config['documento'],
            nivel=admin_config['nivel'],
            activo=1
        )
        
        # self.session.commit() # <--- Correcto que esté quitado
        return admin
    
    def cambiar_password(self, usuario_id: int, password_antigua: str, 
                        password_nueva: str) -> Tuple[bool, str]:
        """
        Cambia la contraseña de un usuario
        """
        usuario = self.usuario_repo.get_by_id(usuario_id)
        
        if not usuario:
            return False, "Usuario no encontrado"
        
        if not verify_password(password_antigua, usuario.password_hash):
            return False, "Contraseña actual incorrecta"
        
        if len(password_nueva) < config.PASSWORD_MIN_LENGTH:
            return False, f"La contraseña debe tener al menos {config.PASSWORD_MIN_LENGTH} caracteres"
        
        # Actualizar contraseña
        nuevo_hash = hash_password(password_nueva)
        self.usuario_repo.update(usuario_id, password_hash=nuevo_hash)
        
        # Registrar actividad
        if self.usuario_actual:
            self.auditoria_repo.registrar_actividad(
                usuario_id=self.usuario_actual.id,
                tipo_actividad="Cambio de Contraseña",
                descripcion=f"Contraseña cambiada para usuario: {usuario.username}"
            )
        
        # self.session.commit() # <--- Correcto que esté quitado
        return True, "Contraseña actualizada exitosamente"
    
    def get_usuarios_activos(self):
        """Obtiene todos los usuarios activos"""
        return self.usuario_repo.get_activos()
    
    def get_todos_usuarios(self):
        """Obtiene todos los usuarios"""
        return self.usuario_repo.get_all()