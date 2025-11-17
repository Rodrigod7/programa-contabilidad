"""
Vista de Dashboard (Resumen general)
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QGroupBox, 
                             QHBoxLayout, QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from app.models.usuario import Usuario
from app.core.database import get_session
from app.services.contabilidad_service import ContabilidadService
from app.services.reportes_service import ReportesService
from app.utils.formatters import formatear_moneda


class DashboardView(QWidget):
    """Vista de dashboard con resumen general"""
    
    def __init__(self, usuario: Usuario):
        super().__init__()
        self.usuario = usuario
        self.init_ui()
        self.actualizar_datos()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title = QLabel("Dashboard - Resumen General")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Contenedor de tarjetas de resumen
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20) # Añadimos espaciado entre tarjetas
        
        # Tarjeta de Activos
        self.activos_label = QLabel("$0.00")
        activos_group = self.crear_tarjeta("Total Activos", self.activos_label)
        cards_layout.addWidget(activos_group)
        
        # Tarjeta de Pasivos
        self.pasivos_label = QLabel("$0.00")
        pasivos_group = self.crear_tarjeta("Total Pasivos", self.pasivos_label)
        cards_layout.addWidget(pasivos_group)
        
        # Tarjeta de Patrimonio
        self.patrimonio_label = QLabel("$0.00")
        patrimonio_group = self.crear_tarjeta("Patrimonio Neto", self.patrimonio_label)
        cards_layout.addWidget(patrimonio_group)
        
        layout.addLayout(cards_layout)
        
        # Botón de actualizar
        btn_actualizar = QPushButton("Actualizar")
        btn_actualizar.clicked.connect(self.actualizar_datos)
        btn_actualizar.setMaximumWidth(150)
        layout.addWidget(btn_actualizar)
        
        layout.addStretch()
        
        self.setLayout(layout)
    
    def crear_tarjeta(self, titulo: str, label_valor: QLabel) -> QGroupBox:
        """Crea una tarjeta de resumen"""
        
        # --- CORRECCIÓN DE LAYOUT ---
        # No usamos el título del QGroupBox.
        # Creamos una etiqueta de título propia dentro del layout.
        group = QGroupBox()
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # 1. Etiqueta de Título (en lugar del título del GroupBox)
        label_titulo = QLabel(titulo)
        label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # (El QSS se encargará del estilo de esta etiqueta)
        
        # 2. Etiqueta de Valor (con el objectName para el QSS)
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        label_valor.setFont(font)
        label_valor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # IMPORTANTE: Asignamos un nombre de objeto para el QSS
        label_valor.setObjectName("valorDashboard") 
        
        # 3. Añadir ambas etiquetas al layout de la tarjeta
        layout.addWidget(label_titulo)
        layout.addWidget(label_valor)
        
        group.setLayout(layout)
        
        # --- FIN DE CORRECCIÓN ---
        
        return group
    
    def actualizar_datos(self):
        """Actualiza los datos del dashboard"""
        try:
            with get_session() as session:
                contabilidad_service = ContabilidadService(session)
                balance = contabilidad_service.obtener_balance_general()
                estado_resultados = contabilidad_service.obtener_estado_resultados()
                
                # Actualizar labels
                self.activos_label.setText(formatear_moneda(balance['total_activo']))
                self.pasivos_label.setText(formatear_moneda(balance['total_pasivo']))
                patrimonio_total = balance['total_patrimonio'] + estado_resultados['resultado_periodo']
                self.patrimonio_label.setText(formatear_moneda(patrimonio_total))
                
        except Exception as e:
            self.activos_label.setText("Error")
            self.pasivos_label.setText("Error")
            self.patrimonio_label.setText("Error")
            # Imprimimos en consola (el log ya lo captura en main.py si es fatal)
            print(f"Error al actualizar dashboard: {e}")