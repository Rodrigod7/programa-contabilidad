"""
Ventana Principal de la Aplicación
"""
from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout,
                             QPushButton, QMessageBox, QStatusBar)
from PyQt6.QtCore import Qt
from app.models.usuario import Usuario
from app.core.database import get_session
from app.services.auth_service import AuthService
from app.gui.views.dashboard_view import DashboardView
from app.gui.views.transacciones_view import TransaccionesView
from app.gui.views.balance_view import BalanceView
from app.gui.views.reportes_view import ReportesView
from app.gui.views.usuarios_view import UsuariosView
from app.utils.logger import app_logger


class MainWindow(QMainWindow):
    """Ventana principal de la aplicación"""
    
    def __init__(self, usuario: Usuario):
        super().__init__()
        self.usuario = usuario
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        # Configuración de la ventana
        self.setWindowTitle(f"ContabilidadPro - {self.usuario.nombre_completo}")
        self.setGeometry(100, 100, 1200, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Tabs
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Crear pestañas según el nivel del usuario
        if self.usuario.es_administrador:
            self.crear_tabs_administrador()
        else:
            self.crear_tabs_trabajador()
        
        # Botón cerrar sesión
        btn_cerrar_sesion = QPushButton("Cerrar Sesión")
        btn_cerrar_sesion.clicked.connect(self.cerrar_sesion)
        btn_cerrar_sesion.setMaximumWidth(150)
        layout.addWidget(btn_cerrar_sesion, alignment=Qt.AlignmentFlag.AlignRight)
        
        # Barra de estado
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.showMessage(f"Usuario: {self.usuario.nombre_completo} ({self.usuario.username})")
        
        app_logger.info(f"Ventana principal cargada para usuario {self.usuario.username}")
    
    def crear_tabs_administrador(self):
        """Crea las pestañas para usuarios administradores"""
        # Dashboard
        self.dashboard_view = DashboardView(self.usuario)
        self.tabs.addTab(self.dashboard_view, "Dashboard")
        
        # Transacciones
        self.transacciones_view = TransaccionesView(self.usuario)
        self.tabs.addTab(self.transacciones_view, "Transacciones")
        
        # Balance
        self.balance_view = BalanceView(self.usuario)
        self.tabs.addTab(self.balance_view, "Balance")
        
        # Reportes
        self.reportes_view = ReportesView(self.usuario)
        self.tabs.addTab(self.reportes_view, "Reportes")
        
        # Usuarios
        self.usuarios_view = UsuariosView(self.usuario)
        self.tabs.addTab(self.usuarios_view, "Usuarios")
    
    def crear_tabs_trabajador(self):
        """Crea las pestañas para usuarios trabajadores"""
        # Solo transacciones (ventas y compras)
        self.transacciones_view = TransaccionesView(self.usuario, modo_simple=True)
        self.tabs.addTab(self.transacciones_view, "Ventas y Compras")
    
    def cerrar_sesion(self):
        """Cierra la sesión del usuario"""
        respuesta = QMessageBox.question(
            self,
            "Cerrar Sesión",
            "¿Está seguro que desea cerrar sesión?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            try:
                with get_session() as session:
                    auth_service = AuthService(session)
                    auth_service.usuario_actual = self.usuario
                    auth_service.cerrar_sesion()
                
                app_logger.info(f"Usuario {self.usuario.username} cerró sesión")
                self.close()
                
            except Exception as e:
                app_logger.error(f"Error al cerrar sesión: {e}")
                QMessageBox.critical(self, "Error", "Error al cerrar sesión")
    
    def closeEvent(self, event):
        """Maneja el evento de cierre de la ventana"""
        event.accept()
