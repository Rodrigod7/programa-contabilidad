"""
Vista de Gestión de Usuarios
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QGroupBox, QMessageBox,
                             QTextEdit, QComboBox)
from PyQt6.QtGui import QFont
from app.models.usuario import Usuario
from app.core.database import get_session
from app.services.auth_service import AuthService
from app.core.constants import NIVEL_TRABAJADOR, NIVEL_ADMINISTRADOR


class UsuariosView(QWidget):
    """Vista para gestión de usuarios"""
    
    def __init__(self, usuario: Usuario):
        super().__init__()
        self.usuario = usuario
        self.init_ui()
        self.actualizar_lista()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title = QLabel("Gestión de Usuarios")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Formulario para crear usuario
        crear_group = QGroupBox("Crear Nuevo Usuario")
        crear_layout = QVBoxLayout()
        
        self.new_username = QLineEdit()
        self.new_username.setPlaceholderText("Nombre de usuario")
        
        self.new_password = QLineEdit()
        self.new_password.setPlaceholderText("Contraseña")
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.new_nombre = QLineEdit()
        self.new_nombre.setPlaceholderText("Nombre")
        
        self.new_apellido = QLineEdit()
        self.new_apellido.setPlaceholderText("Apellido")
        
        self.new_documento = QLineEdit()
        self.new_documento.setPlaceholderText("Documento")
        
        self.new_nivel = QComboBox()
        self.new_nivel.addItems([
            f"{NIVEL_TRABAJADOR} - Trabajador",
            f"{NIVEL_ADMINISTRADOR} - Administrador"
        ])
        
        btn_crear = QPushButton("Crear Usuario")
        btn_crear.clicked.connect(self.crear_usuario)
        
        crear_layout.addWidget(QLabel("Usuario:"))
        crear_layout.addWidget(self.new_username)
        crear_layout.addWidget(QLabel("Contraseña:"))
        crear_layout.addWidget(self.new_password)
        crear_layout.addWidget(QLabel("Nombre:"))
        crear_layout.addWidget(self.new_nombre)
        crear_layout.addWidget(QLabel("Apellido:"))
        crear_layout.addWidget(self.new_apellido)
        crear_layout.addWidget(QLabel("Documento:"))
        crear_layout.addWidget(self.new_documento)
        crear_layout.addWidget(QLabel("Nivel:"))
        crear_layout.addWidget(self.new_nivel)
        crear_layout.addWidget(btn_crear)
        
        crear_group.setLayout(crear_layout)
        layout.addWidget(crear_group)
        
        # Lista de usuarios
        lista_group = QGroupBox("Usuarios Registrados")
        lista_layout = QVBoxLayout()
        
        self.usuarios_text = QTextEdit()
        self.usuarios_text.setReadOnly(True)
        self.usuarios_text.setFont(QFont("Courier New", 10))
        lista_layout.addWidget(self.usuarios_text)
        
        btn_actualizar = QPushButton("Actualizar Lista")
        btn_actualizar.clicked.connect(self.actualizar_lista)
        lista_layout.addWidget(btn_actualizar)
        
        lista_group.setLayout(lista_layout)
        layout.addWidget(lista_group)
        
        self.setLayout(layout)
    
    def crear_usuario(self):
        """Crea un nuevo usuario"""
        username = self.new_username.text().strip()
        password = self.new_password.text()
        nombre = self.new_nombre.text().strip()
        apellido = self.new_apellido.text().strip()
        documento = self.new_documento.text().strip()
        nivel_texto = self.new_nivel.currentText()
        nivel = int(nivel_texto.split(" - ")[0])
        
        if not all([username, password, nombre, apellido, documento]):
            QMessageBox.warning(self, "Error", "Complete todos los campos")
            return
        
        try:
            with get_session() as session:
                auth_service = AuthService(session)
                auth_service.usuario_actual = self.usuario
                exito, mensaje = auth_service.crear_usuario(
                    username, password, nombre, apellido, documento, nivel
                )
                
                if exito:
                    QMessageBox.information(self, "Éxito", mensaje)
                    # Limpiar campos
                    self.new_username.clear()
                    self.new_password.clear()
                    self.new_nombre.clear()
                    self.new_apellido.clear()
                    self.new_documento.clear()
                    self.actualizar_lista()
                else:
                    QMessageBox.critical(self, "Error", mensaje)
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al crear usuario: {str(e)}")
    
    def actualizar_lista(self):
        """Actualiza la lista de usuarios"""
        try:
            with get_session() as session:
                auth_service = AuthService(session)
                usuarios = auth_service.get_todos_usuarios()
                
                texto = "USUARIOS REGISTRADOS\n"
                texto += "=" * 50 + "\n\n"
                
                for usuario in usuarios:
                    nivel_texto = "Administrador" if usuario.nivel == NIVEL_ADMINISTRADOR else "Trabajador"
                    estado = "Activo" if usuario.activo else "Inactivo"
                    
                    texto += f"Usuario: {usuario.username}\n"
                    texto += f"Nombre: {usuario.nombre_completo}\n"
                    texto += f"Documento: {usuario.documento}\n"
                    texto += f"Nivel: {nivel_texto}\n"
                    texto += f"Estado: {estado}\n"
                    texto += f"Creado: {usuario.created_at.strftime('%d/%m/%Y %H:%M')}\n"
                    texto += "-" * 30 + "\n"
                
                self.usuarios_text.setText(texto)
                
        except Exception as e:
            self.usuarios_text.setText(f"Error al cargar usuarios: {str(e)}")
