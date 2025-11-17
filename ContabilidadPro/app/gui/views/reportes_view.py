"""
Vista de Reportes
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, QPushButton,
                             QLabel, QHBoxLayout, QComboBox)
from PyQt6.QtGui import QFont
from app.models.usuario import Usuario
from app.core.database import get_session
from app.services.reportes_service import ReportesService


class ReportesView(QWidget):
    """Vista para generar y mostrar reportes"""
    
    def __init__(self, usuario: Usuario):
        super().__init__()
        self.usuario = usuario
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title = QLabel("Reportes")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Selector de tipo de reporte
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Tipo de Reporte:"))
        
        self.tipo_reporte_combo = QComboBox()
        self.tipo_reporte_combo.addItems([
            "Balance General",
            "Estado de Resultados",
            "Transacciones",
            "Actividades"
        ])
        selector_layout.addWidget(self.tipo_reporte_combo)
        
        btn_generar = QPushButton("Generar Reporte")
        btn_generar.clicked.connect(self.generar_reporte)
        selector_layout.addWidget(btn_generar)
        
        selector_layout.addStretch()
        layout.addLayout(selector_layout)
        
        # Área de texto para mostrar el reporte
        self.reporte_text = QTextEdit()
        self.reporte_text.setReadOnly(True)
        self.reporte_text.setFont(QFont("Courier New", 10))
        layout.addWidget(self.reporte_text)
        
        self.setLayout(layout)
    
    def generar_reporte(self):
        """Genera el reporte seleccionado"""
        tipo = self.tipo_reporte_combo.currentText()
        
        try:
            with get_session() as session:
                reportes_service = ReportesService(session)
                
                if tipo == "Balance General":
                    texto = reportes_service.generar_balance_general_texto()
                elif tipo == "Estado de Resultados":
                    texto = reportes_service.generar_estado_resultados_texto()
                elif tipo == "Transacciones":
                    texto = reportes_service.generar_reporte_transacciones()
                elif tipo == "Actividades":
                    texto = reportes_service.generar_reporte_actividades()
                else:
                    texto = "Tipo de reporte no reconocido"
                
                self.reporte_text.setText(texto)
                
        except Exception as e:
            self.reporte_text.setText(f"Error al generar reporte: {str(e)}")
