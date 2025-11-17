"""
Servicio de Contabilidad - Lógica de negocio principal
"""
from typing import Tuple, Dict, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from app.repositories.cuenta_repository import CuentaRepository
from app.repositories.transaccion_repository import TransaccionRepository
from app.repositories.auditoria_repository import AuditoriaRepository
from app.models.usuario import Usuario
from app.core.constants import *


class ContabilidadService:
    """Servicio principal de lógica contable"""
    
    def __init__(self, session: Session):
        self.session = session
        self.cuenta_repo = CuentaRepository(session)
        self.transaccion_repo = TransaccionRepository(session)
        self.auditoria_repo = AuditoriaRepository(session)
    
    def registrar_venta(self, concepto: str, monto: float, usuario: Usuario) -> Tuple[bool, str]:
        """
        Registra una venta
        """
        if monto <= 0:
            return False, "El monto debe ser mayor a cero"
        
        # Buscar o crear cuenta de ingresos por ventas
        cuenta_ingreso = self.cuenta_repo.get_by_codigo("ING-VENTAS")
        if not cuenta_ingreso:
            cuenta_ingreso = self.cuenta_repo.create(
                codigo="ING-VENTAS",
                nombre="Ingresos por Ventas",
                tipo=TIPO_INGRESO,
                naturaleza=NATURALEZA_ACREEDORA,
                saldo=0.0,
                activa=1
            )
        
        # Crear transacción
        self.transaccion_repo.create(
            fecha=datetime.now(),
            concepto=f"Venta: {concepto}",
            monto=monto,
            tipo=TIPO_TRANSACCION_VENTA,
            cuenta_id=cuenta_ingreso.id,
            usuario_id=usuario.id
        )
        
        # Actualizar saldo de la cuenta
        self.cuenta_repo.sumar_al_saldo(cuenta_ingreso.id, monto)
        
        # Registrar actividad
        self.auditoria_repo.registrar_actividad(
            usuario_id=usuario.id,
            tipo_actividad=ACTIVIDAD_VENTA,
            descripcion=f"Venta registrada: {concepto} - ${monto:,.2f}"
        )
        
        # self.session.commit() # <--- ELIMINADO
        return True, "Venta registrada exitosamente"
    
    def registrar_compra(self, concepto: str, monto: float, usuario: Usuario) -> Tuple[bool, str]:
        """
        Registra una compra
        """
        if monto <= 0:
            return False, "El monto debe ser mayor a cero"
        
        # Buscar o crear cuenta de gastos por compras
        cuenta_gasto = self.cuenta_repo.get_by_codigo("GAS-COMPRAS")
        if not cuenta_gasto:
            cuenta_gasto = self.cuenta_repo.create(
                codigo="GAS-COMPRAS",
                nombre="Gastos por Compras",
                tipo=TIPO_GASTO,
                naturaleza=NATURALEZA_DEUDORA,
                saldo=0.0,
                activa=1
            )
        
        # Crear transacción
        self.transaccion_repo.create(
            fecha=datetime.now(),
            concepto=f"Compra: {concepto}",
            monto=monto,
            tipo=TIPO_TRANSACCION_COMPRA,
            cuenta_id=cuenta_gasto.id,
            usuario_id=usuario.id
        )
        
        # Actualizar saldo de la cuenta
        self.cuenta_repo.sumar_al_saldo(cuenta_gasto.id, monto)
        
        # Registrar actividad
        self.auditoria_repo.registrar_actividad(
            usuario_id=usuario.id,
            tipo_actividad=ACTIVIDAD_COMPRA,
            descripcion=f"Compra registrada: {concepto} - ${monto:,.2f}"
        )
        
        # self.session.commit() # <--- ELIMINADO
        return True, "Compra registrada exitosamente"
    
    def registrar_transaccion_cuenta(self, tipo_cuenta: str, concepto: str, 
                                     monto: float, usuario: Usuario) -> Tuple[bool, str]:
        """
        Registra una transacción en una cuenta específica
        """
        if monto <= 0:
            return False, "El monto debe ser mayor a cero"
        
        if tipo_cuenta not in TIPOS_CUENTA:
            return False, "Tipo de cuenta inválido"
        
        # Buscar o crear cuenta
        codigo = self._generar_codigo_cuenta(tipo_cuenta, concepto)
        cuenta = self.cuenta_repo.get_by_codigo(codigo)
        
        if not cuenta:
            naturaleza = self._determinar_naturaleza(tipo_cuenta)
            cuenta = self.cuenta_repo.create(
                codigo=codigo,
                nombre=concepto,
                tipo=tipo_cuenta,
                naturaleza=naturaleza,
                saldo=0.0,
                activa=1
            )
        
        # Crear transacción
        self.transaccion_repo.create(
            fecha=datetime.now(),
            concepto=concepto,
            monto=monto,
            tipo=TIPO_TRANSACCION_GENERAL,
            cuenta_id=cuenta.id,
            usuario_id=usuario.id
        )
        
        # Actualizar saldo
        self.cuenta_repo.sumar_al_saldo(cuenta.id, monto)
        
        # Registrar actividad
        self.auditoria_repo.registrar_actividad(
            usuario_id=usuario.id,
            tipo_actividad=ACTIVIDAD_CREAR_TRANSACCION,
            descripcion=f"Transacción: {tipo_cuenta} - {concepto} - ${monto:,.2f}"
        )
        
        # self.session.commit() # <--- ELIMINADO
        return True, "Transacción registrada exitosamente"
    
    def obtener_balance_general(self) -> Dict:
        # ... (el resto del archivo no cambia) ...
        balance = {
            'activo_corriente': {},
            'activo_no_corriente': {},
            'pasivo_corriente': {},
            'pasivo_no_corriente': {},
            'patrimonio': {}
        }
        
        # Activos
        for cuenta in self.cuenta_repo.get_by_tipo(TIPO_ACTIVO_CORRIENTE):
            balance['activo_corriente'][cuenta.nombre] = cuenta.saldo
        
        for cuenta in self.cuenta_repo.get_by_tipo(TIPO_ACTIVO_NO_CORRIENTE):
            balance['activo_no_corriente'][cuenta.nombre] = cuenta.saldo
        
        # Pasivos
        for cuenta in self.cuenta_repo.get_by_tipo(TIPO_PASIVO_CORRIENTE):
            balance['pasivo_corriente'][cuenta.nombre] = cuenta.saldo
        
        for cuenta in self.cuenta_repo.get_by_tipo(TIPO_PASIVO_NO_CORRIENTE):
            balance['pasivo_no_corriente'][cuenta.nombre] = cuenta.saldo
        
        # Patrimonio
        for cuenta in self.cuenta_repo.get_by_tipo(TIPO_CAPITAL):
            balance['patrimonio'][cuenta.nombre] = cuenta.saldo
        
        for cuenta in self.cuenta_repo.get_by_tipo(TIPO_RESERVAS):
            balance['patrimonio'][cuenta.nombre] = cuenta.saldo
        
        # Calcular totales
        balance['total_activo_corriente'] = sum(balance['activo_corriente'].values())
        balance['total_activo_no_corriente'] = sum(balance['activo_no_corriente'].values())
        balance['total_activo'] = balance['total_activo_corriente'] + balance['total_activo_no_corriente']
        
        balance['total_pasivo_corriente'] = sum(balance['pasivo_corriente'].values())
        balance['total_pasivo_no_corriente'] = sum(balance['pasivo_no_corriente'].values())
        balance['total_pasivo'] = balance['total_pasivo_corriente'] + balance['total_pasivo_no_corriente']
        
        balance['total_patrimonio'] = sum(balance['patrimonio'].values())
        
        return balance
    
    def obtener_estado_resultados(self) -> Dict:
        """
        Genera el estado de resultados
        """
        resultado = {
            'ingresos': {},
            'gastos': {}
        }
        
        # Ingresos
        for cuenta in self.cuenta_repo.get_by_tipo(TIPO_INGRESO):
            resultado['ingresos'][cuenta.nombre] = cuenta.saldo
        
        # Gastos
        for cuenta in self.cuenta_repo.get_by_tipo(TIPO_GASTO):
            resultado['gastos'][cuenta.nombre] = cuenta.saldo
        
        # Calcular totales
        resultado['total_ingresos'] = sum(resultado['ingresos'].values())
        resultado['total_gastos'] = sum(resultado['gastos'].values())
        resultado['resultado_periodo'] = resultado['total_ingresos'] - resultado['total_gastos']
        
        return resultado
    
    def _generar_codigo_cuenta(self, tipo: str, concepto: str) -> str:
        """Genera un código único para una cuenta"""
        prefijos = {
            TIPO_ACTIVO_CORRIENTE: "AC",
            TIPO_ACTIVO_NO_CORRIENTE: "ANC",
            TIPO_PASIVO_CORRIENTE: "PC",
            TIPO_PASIVO_NO_CORRIENTE: "PNC",
            TIPO_CAPITAL: "CAP",
            TIPO_RESERVAS: "RES",
            TIPO_INGRESO: "ING",
            TIPO_GASTO: "GAS"
        }
        
        prefijo = prefijos.get(tipo, "GEN")
        concepto_limpio = concepto.replace(" ", "-")[:20].upper()
        return f"{prefijo}-{concepto_limpio}"
    
    def _determinar_naturaleza(self, tipo: str) -> str:
        """Determina la naturaleza de una cuenta según su tipo"""
        cuentas_deudoras = [TIPO_ACTIVO_CORRIENTE, TIPO_ACTIVO_NO_CORRIENTE, TIPO_GASTO]
        return NATURALEZA_DEUDORA if tipo in cuentas_deudoras else NATURALEZA_ACREEDORA