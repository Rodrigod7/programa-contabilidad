"""
Servicio de Reportes
"""
from typing import Dict, List
from datetime import datetime
from app.repositories.transaccion_repository import TransaccionRepository
from app.repositories.auditoria_repository import AuditoriaRepository
from app.services.contabilidad_service import ContabilidadService
from sqlalchemy.orm import Session


class ReportesService:
    """Servicio para generación de reportes"""
    
    def __init__(self, session: Session):
        self.session = session
        self.contabilidad_service = ContabilidadService(session)
        self.transaccion_repo = TransaccionRepository(session)
        self.auditoria_repo = AuditoriaRepository(session)
    
    def generar_balance_general_texto(self) -> str:
        """
        Genera el balance general en formato texto
        
        Returns:
            String con el balance formateado
        """
        balance = self.contabilidad_service.obtener_balance_general()
        
        texto = "=" * 60 + "\n"
        texto += "BALANCE GENERAL\n"
        texto += f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        texto += "=" * 60 + "\n\n"
        
        # ACTIVO
        texto += "ACTIVO\n" + "-" * 30 + "\n"
        texto += "ACTIVO CORRIENTE:\n"
        for cuenta, monto in balance['activo_corriente'].items():
            texto += f"  {cuenta}: ${monto:,.2f}\n"
        texto += f"  TOTAL ACTIVO CORRIENTE: ${balance['total_activo_corriente']:,.2f}\n\n"
        
        texto += "ACTIVO NO CORRIENTE:\n"
        for cuenta, monto in balance['activo_no_corriente'].items():
            texto += f"  {cuenta}: ${monto:,.2f}\n"
        texto += f"  TOTAL ACTIVO NO CORRIENTE: ${balance['total_activo_no_corriente']:,.2f}\n\n"
        texto += f"TOTAL ACTIVO: ${balance['total_activo']:,.2f}\n\n"
        
        # PASIVO
        texto += "PASIVO\n" + "-" * 30 + "\n"
        texto += "PASIVO CORRIENTE:\n"
        for cuenta, monto in balance['pasivo_corriente'].items():
            texto += f"  {cuenta}: ${monto:,.2f}\n"
        texto += f"  TOTAL PASIVO CORRIENTE: ${balance['total_pasivo_corriente']:,.2f}\n\n"
        
        texto += "PASIVO NO CORRIENTE:\n"
        for cuenta, monto in balance['pasivo_no_corriente'].items():
            texto += f"  {cuenta}: ${monto:,.2f}\n"
        texto += f"  TOTAL PASIVO NO CORRIENTE: ${balance['total_pasivo_no_corriente']:,.2f}\n\n"
        texto += f"TOTAL PASIVO: ${balance['total_pasivo']:,.2f}\n\n"
        
        # PATRIMONIO
        texto += "PATRIMONIO NETO\n" + "-" * 30 + "\n"
        for cuenta, monto in balance['patrimonio'].items():
            texto += f"  {cuenta}: ${monto:,.2f}\n"
        
        # Agregar resultado del período
        estado_resultados = self.contabilidad_service.obtener_estado_resultados()
        resultado_periodo = estado_resultados['resultado_periodo']
        texto += f"  Resultado del Período: ${resultado_periodo:,.2f}\n"
        texto += f"TOTAL PATRIMONIO NETO: ${balance['total_patrimonio'] + resultado_periodo:,.2f}\n\n"
        
        # VERIFICACIÓN
        texto += "=" * 60 + "\n"
        texto += "VERIFICACIÓN ECUACIÓN CONTABLE\n"
        texto += "=" * 60 + "\n"
        texto += f"ACTIVO: ${balance['total_activo']:,.2f}\n"
        total_pasivo_patrimonio = balance['total_pasivo'] + balance['total_patrimonio'] + resultado_periodo
        texto += f"PASIVO + PATRIMONIO NETO: ${total_pasivo_patrimonio:,.2f}\n"
        
        diferencia = abs(balance['total_activo'] - total_pasivo_patrimonio)
        if diferencia < 0.01:
            texto += "✓ La ecuación contable está balanceada\n"
        else:
            texto += f"✗ ERROR: La ecuación contable NO está balanceada (diferencia: ${diferencia:,.2f})\n"
        
        return texto
    
    def generar_estado_resultados_texto(self) -> str:
        """
        Genera el estado de resultados en formato texto
        
        Returns:
            String con el estado de resultados formateado
        """
        resultado = self.contabilidad_service.obtener_estado_resultados()
        
        texto = "=" * 60 + "\n"
        texto += "ESTADO DE RESULTADOS\n"
        texto += f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        texto += "=" * 60 + "\n\n"
        
        # INGRESOS
        texto += "INGRESOS:\n"
        for concepto, monto in resultado['ingresos'].items():
            texto += f"  {concepto}: ${monto:,.2f}\n"
        texto += f"  TOTAL INGRESOS: ${resultado['total_ingresos']:,.2f}\n\n"
        
        # GASTOS
        texto += "GASTOS:\n"
        for concepto, monto in resultado['gastos'].items():
            texto += f"  {concepto}: ${monto:,.2f}\n"
        texto += f"  TOTAL GASTOS: ${resultado['total_gastos']:,.2f}\n\n"
        
        # RESULTADO
        resultado_periodo = resultado['resultado_periodo']
        texto += f"RESULTADO DEL PERÍODO: ${resultado_periodo:,.2f}\n"
        
        if resultado_periodo > 0:
            texto += "(GANANCIA)\n"
        elif resultado_periodo < 0:
            texto += "(PÉRDIDA)\n"
        else:
            texto += "(PUNTO DE EQUILIBRIO)\n"
        
        return texto
    
    def generar_reporte_transacciones(self, limite: int = 50) -> str:
        """
        Genera un reporte de las últimas transacciones
        
        Args:
            limite: Número de transacciones a mostrar
            
        Returns:
            String con el reporte
        """
        transacciones = self.transaccion_repo.get_all()
        transacciones = sorted(transacciones, key=lambda x: x.fecha, reverse=True)[:limite]
        
        texto = "=" * 80 + "\n"
        texto += "REPORTE DE TRANSACCIONES\n"
        texto += f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        texto += f"Últimas {len(transacciones)} transacciones\n"
        texto += "=" * 80 + "\n\n"
        
        for t in transacciones:
            texto += f"Fecha: {t.fecha.strftime('%d/%m/%Y %H:%M')}\n"
            texto += f"Tipo: {t.tipo}\n"
            texto += f"Concepto: {t.concepto}\n"
            texto += f"Monto: ${t.monto:,.2f}\n"
            texto += f"Cuenta: {t.cuenta.nombre if t.cuenta else 'N/A'}\n"
            texto += f"Usuario: {t.usuario.nombre_completo if t.usuario else 'N/A'}\n"
            texto += "-" * 80 + "\n"
        
        return texto
    
    def generar_reporte_actividades(self, usuario_id: int = None, limite: int = 100) -> str:
        """
        Genera un reporte de actividades
        
        Args:
            usuario_id: ID del usuario (None para todas las actividades)
            limite: Número de actividades a mostrar
            
        Returns:
            String con el reporte
        """
        if usuario_id:
            actividades = self.auditoria_repo.get_by_usuario(usuario_id)[:limite]
            titulo = f"Actividades del usuario ID {usuario_id}"
        else:
            actividades = self.auditoria_repo.get_recientes(limite)
            titulo = "Todas las actividades"
        
        texto = "=" * 80 + "\n"
        texto += f"REPORTE DE ACTIVIDADES - {titulo}\n"
        texto += f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        texto += "=" * 80 + "\n\n"
        
        for act in actividades:
            texto += f"Usuario: {act.usuario.username} ({act.usuario.nombre_completo})\n"
            texto += f"Fecha/Hora: {act.fecha_hora.strftime('%d/%m/%Y %H:%M:%S')}\n"
            texto += f"Tipo: {act.tipo_actividad}\n"
            texto += f"Descripción: {act.descripcion}\n"
            texto += "-" * 80 + "\n"
        
        return texto
