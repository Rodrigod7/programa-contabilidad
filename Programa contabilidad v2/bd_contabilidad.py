import json
import os

# Obtener la ruta del directorio donde está este script
DIRECTORIO_SCRIPT = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_DATOS = os.path.join(DIRECTORIO_SCRIPT, "datos_contables.json")

def guardar_datos(contabilidad):
    datos = {
        "activo_corriente": contabilidad.activo_corriente,
        "activo_no_corriente": contabilidad.activo_no_corriente,
        "pasivo_corriente": contabilidad.pasivo_corriente,
        "pasivo_no_corriente": contabilidad.pasivo_no_corriente,
        "capital": contabilidad.capital,
        "reservas": contabilidad.reservas,
        "resultados_acumulados": contabilidad.resultados_acumulados,
        "ingresos": contabilidad.ingresos,
        "gastos": contabilidad.gastos
    }
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4)
        
def cargar_datos(contabilidad):
    if not os.path.exists(ARCHIVO_DATOS) or os.path.getsize(ARCHIVO_DATOS) == 0:
        return  # No hacer nada si no existe o está vacío

    with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
        try:
            datos = json.load(f)
        except json.JSONDecodeError:
            return  # No hacer nada si el archivo no es JSON válido

        contabilidad.activo_corriente = datos.get("activo_corriente", {})
        contabilidad.activo_no_corriente = datos.get("activo_no_corriente", {})
        contabilidad.pasivo_corriente = datos.get("pasivo_corriente", {})
        contabilidad.pasivo_no_corriente = datos.get("pasivo_no_corriente", {})
        contabilidad.capital = datos.get("capital", 0)
        contabilidad.reservas = datos.get("reservas", 0)
        contabilidad.resultados_acumulados = datos.get("resultados_acumulados", 0)
        contabilidad.ingresos = datos.get("ingresos", {})
        contabilidad.gastos = datos.get("gastos", {})

def inicializar_datos(contabilidad):
    """Carga los datos al inicializar el sistema"""
    cargar_datos(contabilidad)