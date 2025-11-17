"""
Vista de Login
"""
# Importamos QFormLayout
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QGroupBox,
                             QFormLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from app.core.database import get_session
from app.services.auth_service import AuthService
from app.models.usuario import Usuario


class LoginView(QDialog):
    """Ventana de inicio de sesión"""
    
    def __init__(self):
        super().__init__()
        self.usuario_autenticado = None
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        self.setWindowTitle("ContabilidadPro - Inicio de Sesión")
        # Aumenté un poco la altura para que quepa todo
        self.setFixedSize(400, 320) 
        self.setModal(True)
        
        # Layout principal
        layout = QVBoxLayout()
        layout.setSpacing(15) # Reduje el espaciado
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Título
        title_label = QLabel("Sistema de Contabilidad")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        subtitle_label = QLabel("ContabilidadPro")
        subtitle_font = QFont()
        subtitle_font.setPointSize(10)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle_label)

        # --- INICIO DEL CAMBIO ---
        # Usar un QFormLayout para los campos de entrada
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        self.username_input.setMinimumHeight(35)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(35)
        self.password_input.returnPressed.connect(self.login)
        
        # Añadir filas al QFormLayout (esto arregla el solapamiento)
        form_layout.addRow(QLabel("Usuario:"), self.username_input)
        form_layout.addRow(QLabel("Contraseña:"), self.password_input)
        
        # Añadir el form_layout al layout principal
        layout.addLayout(form_layout)
        # --- FIN DEL CAMBIO ---
        
        # Botón de login
        login_btn = QPushButton("Iniciar Sesión")
        login_btn.setMinimumHeight(40)
        login_btn.clicked.connect(self.login)
        
        # Fix para el foco feo en el botón (opcional pero recomendado)
        login_btn.setStyleSheet("""
            QPushButton:focus { 
                outline: none; 
                border: 2px solid #5a90d6; 
            }
        """)
        
        layout.addWidget(login_btn)
        
        # Información por defecto
        info_group = QGroupBox("Acceso por defecto")
        info_layout = QVBoxLayout()
        info_layout.addWidget(QLabel("Usuario: Ivan"))
        info_layout.addWidget(QLabel("Contraseña: Rodri2008"))
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        layout.addStretch() # Empuja todo hacia arriba
        
        self.setLayout(layout)
        
        # Focus en el campo de usuario
        self.username_input.setFocus()
    
    def login(self):
        """Procesa el inicio de sesión"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos")
            return
        
        try:
            with get_session() as session:
                auth_service = AuthService(session)
                exito, mensaje, usuario = auth_service.autenticar(username, password)
                
                if exito:
                    self.usuario_autenticado = usuario
                    self.accept()
                else:
                    QMessageBox.critical(self, "Error de Autenticación", mensaje)
                    self.password_input.clear()
                    self.password_input.setFocus()
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al autenticar: {str(e)}")