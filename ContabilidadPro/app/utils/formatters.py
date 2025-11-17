"""
Formateadores de datos
"""
from datetime import datetime
from typing import Optional


def formatear_moneda(monto: float, simbolo: str = "$") -> str:
    """
    Formatea un monto como moneda
    
    Args:
        monto: Monto a formatear
        simbolo: Símbolo de moneda
        
    Returns:
        String formateado
    """
    return f"{simbolo}{monto:,.2f}"


def formatear_fecha(fecha: datetime, formato: str = "%d/%m/%Y") -> str:
    """
    Formatea una fecha
    
    Args:
        fecha: Fecha a formatear
        formato: Formato deseado
        
    Returns:
        String con la fecha formateada
    """
    if not fecha:
        return ""
    return fecha.strftime(formato)


def formatear_fecha_hora(fecha: datetime, formato: str = "%d/%m/%Y %H:%M:%S") -> str:
    """
    Formatea una fecha y hora
    
    Args:
        fecha: Fecha a formatear
        formato: Formato deseado
        
    Returns:
        String con la fecha y hora formateadas
    """
    if not fecha:
        return ""
    return fecha.strftime(formato)


def formatear_porcentaje(valor: float, decimales: int = 2) -> str:
    """
    Formatea un valor como porcentaje
    
    Args:
        valor: Valor a formatear (0.15 = 15%)
        decimales: Número de decimales
        
    Returns:
        String formateado
    """
    return f"{valor * 100:.{decimales}f}%"


def formatear_numero(numero: float, decimales: int = 2) -> str:
    """
    Formatea un número con separadores de miles
    
    Args:
        numero: Número a formatear
        decimales: Número de decimales
        
    Returns:
        String formateado
    """
    return f"{numero:,.{decimales}f}"


def limpiar_monto(texto: str) -> Optional[float]:
    """
    Convierte un string a monto numérico
    
    Args:
        texto: Texto a convertir
        
    Returns:
        Float o None si no es válido
    """
    try:
        # Remover símbolos de moneda y espacios
        texto_limpio = texto.replace("$", "").replace(" ", "").replace(",", "")
        return float(texto_limpio)
    except (ValueError, AttributeError):
        return None


def capitalizar_texto(texto: str) -> str:
    """
    Capitaliza un texto (primera letra de cada palabra en mayúscula)
    
    Args:
        texto: Texto a capitalizar
        
    Returns:
        Texto capitalizado
    """
    return texto.title() if texto else ""


def truncar_texto(texto: str, max_length: int = 50, sufijo: str = "...") -> str:
    """
    Trunca un texto si excede la longitud máxima
    
    Args:
        texto: Texto a truncar
        max_length: Longitud máxima
        sufijo: Sufijo a agregar si se trunca
        
    Returns:
        Texto truncado
    """
    if not texto or len(texto) <= max_length:
        return texto
    return texto[:max_length - len(sufijo)] + sufijo
