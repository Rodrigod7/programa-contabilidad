import hashlib
from datetime import datetime

class Usuario:
    def __init__(self, username, password, nombre, apellido, documento, nivel):
        self.username = username
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.nombre = nombre
        self.apellido = apellido
        self.documento = documento
        self.nivel = nivel
        self.fecha_creacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

class SistemaUsuarios:
    def __init__(self):
        self.usuarios = {}
        self.usuario_actual = None
        self.log_actividades = []
        
        # Importar funciones de persistencia
        try:
            from bd_usuarios import cargar_usuarios, cargar_actividades
            # Cargar usuarios y actividades guardados
            cargar_usuarios(self)
            cargar_actividades(self)
        except ImportError:
            pass  # Si no existe el archivo bd_usuarios.py, continuar sin cargar
        
        # Crear admin por defecto solo si no existe
        if "admin" not in self.usuarios:
            self.crear_admin_default()

    def crear_admin_default(self):
        """Crea el usuario administrador por defecto"""
        admin = Usuario("Ivan", "Rodri2008", "Ricardo Ivan", "Espinoza", "20452423", 2)
        self.usuarios["Ivan"] = admin
        self._guardar_usuarios()

    def crear_usuario(self, username, password, nombre, apellido, documento, nivel):
        """Crea un nuevo usuario y lo guarda"""
        if username in self.usuarios:
            return False, "El usuario ya existe"
        
        usuario = Usuario(username, password, nombre, apellido, documento, nivel)
        self.usuarios[username] = usuario
        
        # Guardar usuarios
        self._guardar_usuarios()
        
        # Registrar actividad
        self.registrar_actividad(f"Usuario creado: {username} ({nombre} {apellido})")
        
        return True, "Usuario creado exitosamente"

    def autenticar(self, username, password):
        """Autentica un usuario"""
        if username not in self.usuarios:
            return False, "Usuario no encontrado"
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if self.usuarios[username].password_hash == password_hash:
            self.usuario_actual = self.usuarios[username]
            self.registrar_actividad(f"Inicio de sesión: {username}")
            return True, "Autenticación exitosa"
        
        return False, "Contraseña incorrecta"

    def registrar_actividad(self, descripcion):
        """Registra una actividad en el log"""
        if self.usuario_actual:
            self.log_actividades.append({
                'usuario': self.usuario_actual.username,
                'nombre_completo': f"{self.usuario_actual.nombre} {self.usuario_actual.apellido}",
                'descripcion': descripcion,
                'fecha_hora': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            })
            
            # Guardar actividades
            self._guardar_actividades()

    def cerrar_sesion(self):
        """Cierra la sesión del usuario actual"""
        if self.usuario_actual:
            self.registrar_actividad(f"Cierre de sesión: {self.usuario_actual.username}")
            self.usuario_actual = None

    def _guardar_usuarios(self):
        """Método privado para guardar usuarios"""
        try:
            from bd_usuarios import guardar_usuarios
            guardar_usuarios(self)
        except ImportError:
            pass  # Si no existe el archivo bd_usuarios.py, no guardar

    def _guardar_actividades(self):
        """Método privado para guardar actividades"""
        try:
            from bd_usuarios import guardar_actividades
            guardar_actividades(self)
        except ImportError:
            pass  