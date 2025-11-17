"""
Vista de Transacciones (Ventas y Compras)
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QGroupBox, QMessageBox,
                             QComboBox)
from PyQt6.QtGui import QFont
from app.models.usuario import Usuario
from app.core.database import get_session
from app.services.contabilidad_service import ContabilidadService
from app.services.validacion_service import ValidacionService
from app.utils.formatters import limpiar_monto
from app.core.constants import TIPOS_CUENTA


class TransaccionesView(QWidget):
    """Vista para registro de transacciones"""
    
    def __init__(self, usuario: Usuario, modo_simple: bool = False):
        super().__init__()
        self.usuario = usuario
        self.modo_simple = modo_simple  # True = solo ventas y compras
        self.validacion_service = ValidacionService()
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title = QLabel("Registro de Ventas y Compras" if self.modo_simple else "Registro de Transacciones")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Formulario de Venta
        venta_group = QGroupBox("Registrar Venta")
        venta_layout = QVBoxLayout()
        
        self.venta_concepto = QLineEdit()
        self.venta_concepto.setPlaceholderText("Concepto de la venta")
        
        self.venta_monto = QLineEdit()
        self.venta_monto.setPlaceholderText("Monto ($)")
        
        btn_venta = QPushButton("Registrar Venta")
        btn_venta.clicked.connect(self.registrar_venta)
        
        venta_layout.addWidget(QLabel("Concepto:"))
        venta_layout.addWidget(self.venta_concepto)
        venta_layout.addWidget(QLabel("Monto:"))
        venta_layout.addWidget(self.venta_monto)
        venta_layout.addWidget(btn_venta)
        
        venta_group.setLayout(venta_layout)
        layout.addWidget(venta_group)
        
        # Formulario de Compra
        compra_group = QGroupBox("Registrar Compra")
        compra_layout = QVBoxLayout()
        
        self.compra_concepto = QLineEdit()
        self.compra_concepto.setPlaceholderText("Concepto de la compra")
        
        self.compra_monto = QLineEdit()
        self.compra_monto.setPlaceholderText("Monto ($)")
        
        btn_compra = QPushButton("Registrar Compra")
        btn_compra.clicked.connect(self.registrar_compra)
        
        compra_layout.addWidget(QLabel("Concepto:"))
        compra_layout.addWidget(self.compra_concepto)
        compra_layout.addWidget(QLabel("Monto:"))
        compra_layout.addWidget(self.compra_monto)
        compra_layout.addWidget(btn_compra)
        
        compra_group.setLayout(compra_layout)
        layout.addWidget(compra_group)
        
        # Solo para administradores: transacciones generales
        if not self.modo_simple:
            general_group = QGroupBox("Transacción General")
            general_layout = QVBoxLayout()
            
            self.tipo_combo = QComboBox()
            self.tipo_combo.addItems(TIPOS_CUENTA)
            
            self.general_concepto = QLineEdit()
            self.general_concepto.setPlaceholderText("Concepto")
            
            self.general_monto = QLineEdit()
            self.general_monto.setPlaceholderText("Monto ($)")
            
            btn_general = QPushButton("Registrar Transacción")
            btn_general.clicked.connect(self.registrar_general)
            
            general_layout.addWidget(QLabel("Tipo de Cuenta:"))
            general_layout.addWidget(self.tipo_combo)
            general_layout.addWidget(QLabel("Concepto:"))
            general_layout.addWidget(self.general_concepto)
            general_layout.addWidget(QLabel("Monto:"))
            general_layout.addWidget(self.general_monto)
            general_layout.addWidget(btn_general)
            
            general_group.setLayout(general_layout)
            layout.addWidget(general_group)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def registrar_venta(self):
        """Registra una venta"""
        concepto = self.venta_concepto.text().strip()
        monto_texto = self.venta_monto.text().strip()
        
        # Validar
        if not concepto:
            QMessageBox.warning(self, "Error", "Ingrese el concepto de la venta")
            return
        
        monto = limpiar_monto(monto_texto)
        if monto is None:
            QMessageBox.warning(self, "Error", "Ingrese un monto válido")
            return
        
        valido, mensaje = self.validacion_service.validar_monto(monto)
        if not valido:
            QMessageBox.warning(self, "Error", mensaje)
            return
        
        # Registrar
        try:
            with get_session() as session:
                contabilidad_service = ContabilidadService(session)
                exito, mensaje = contabilidad_service.registrar_venta(concepto, monto, self.usuario)
                
                if exito:
                    QMessageBox.information(self, "Éxito", mensaje)
                    self.venta_concepto.clear()
                    self.venta_monto.clear()
                    self.venta_concepto.setFocus()
                else:
                    QMessageBox.critical(self, "Error", mensaje)
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al registrar venta: {str(e)}")
    
    def registrar_compra(self):
        """Registra una compra"""
        concepto = self.compra_concepto.text().strip()
        monto_texto = self.compra_monto.text().strip()
        
        # Validar
        if not concepto:
            QMessageBox.warning(self, "Error", "Ingrese el concepto de la compra")
            return
        
        monto = limpiar_monto(monto_texto)
        if monto is None:
            QMessageBox.warning(self, "Error", "Ingrese un monto válido")
            return
        
        valido, mensaje = self.validacion_service.validar_monto(monto)
        if not valido:
            QMessageBox.warning(self, "Error", mensaje)
            return
        
        # Registrar
        try:
            with get_session() as session:
                contabilidad_service = ContabilidadService(session)
                exito, mensaje = contabilidad_service.registrar_compra(concepto, monto, self.usuario)
                
                if exito:
                    QMessageBox.information(self, "Éxito", mensaje)
                    self.compra_concepto.clear()
                    self.compra_monto.clear()
                    self.compra_concepto.setFocus()
                else:
                    QMessageBox.critical(self, "Error", mensaje)
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al registrar compra: {str(e)}")
    
    def registrar_general(self):
        """Registra una transacción general"""
        tipo = self.tipo_combo.currentText()
        concepto = self.general_concepto.text().strip()
        monto_texto = self.general_monto.text().strip()
        
        # Validar
        if not concepto:
            QMessageBox.warning(self, "Error", "Ingrese el concepto")
            return
        
        monto = limpiar_monto(monto_texto)
        if monto is None:
            QMessageBox.warning(self, "Error", "Ingrese un monto válido")
            return
        
        valido, mensaje = self.validacion_service.validar_monto(monto)
        if not valido:
            QMessageBox.warning(self, "Error", mensaje)
            return
        
        # Registrar
        try:
            with get_session() as session:
                contabilidad_service = ContabilidadService(session)
                exito, mensaje = contabilidad_service.registrar_transaccion_cuenta(
                    tipo, concepto, monto, self.usuario
                )
                
                if exito:
                    QMessageBox.information(self, "Éxito", mensaje)
                    self.general_concepto.clear()
                    self.general_monto.clear()
                    self.general_concepto.setFocus()
                else:
                    QMessageBox.critical(self, "Error", mensaje)
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al registrar transacción: {str(e)}")
