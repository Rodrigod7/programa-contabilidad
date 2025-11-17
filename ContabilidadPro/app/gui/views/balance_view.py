"""
Vista de Balance General
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, QPushButton,
                             QLabel)
from PyQt6.QtGui import QFont
from app.models.usuario import Usuario
from app.core.database import get_session
from app.services.reportes_service import ReportesService


class BalanceView(QWidget):
    """Vista para mostrar el balance general"""
    
    def __init__(self, usuario: Usuario):
        super().__init__()
        self.usuario = usuario
        self.init_ui()
        self.actualizar_balance()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title = QLabel("Balance General")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Área de texto para mostrar el balance
        self.balance_text = QTextEdit()
        self.balance_text.setReadOnly(True)
        self.balance_text.setFont(QFont("Courier New", 10))
        layout.addWidget(self.balance_text)
        
        # Botón actualizar
        btn_actualizar = QPushButton("Actualizar Balance")
        btn_actualizar.clicked.connect(self.actualizar_balance)
        btn_actualizar.setMaximumWidth(200)
        layout.addWidget(btn_actualizar)
        
        self.setLayout(layout)
    
    def actualizar_balance(self):
        """Actualiza el balance general"""
        try:
            with get_session() as session:
                reportes_service = ReportesService(session)
                balance_texto = reportes_service.generar_balance_general_texto()
                self.balance_text.setText(balance_texto)
        except Exception as e:
            self.balance_text.setText(f"Error al generar balance: {str(e)}")
