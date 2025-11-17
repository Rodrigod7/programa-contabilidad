"""
Constantes globales de la aplicación
"""

# Niveles de usuario
NIVEL_TRABAJADOR = 1
NIVEL_ADMINISTRADOR = 2

NIVELES_USUARIO = {
    NIVEL_TRABAJADOR: "Trabajador",
    NIVEL_ADMINISTRADOR: "Administrador"
}

# Tipos de cuentas contables
TIPO_ACTIVO_CORRIENTE = "Activo Corriente"
TIPO_ACTIVO_NO_CORRIENTE = "Activo No Corriente"
TIPO_PASIVO_CORRIENTE = "Pasivo Corriente"
TIPO_PASIVO_NO_CORRIENTE = "Pasivo No Corriente"
TIPO_CAPITAL = "Capital"
TIPO_RESERVAS = "Reservas"
TIPO_INGRESO = "Ingreso"
TIPO_GASTO = "Gasto"

TIPOS_CUENTA = [
    TIPO_ACTIVO_CORRIENTE,
    TIPO_ACTIVO_NO_CORRIENTE,
    TIPO_PASIVO_CORRIENTE,
    TIPO_PASIVO_NO_CORRIENTE,
    TIPO_CAPITAL,
    TIPO_RESERVAS,
    TIPO_INGRESO,
    TIPO_GASTO
]

# Naturaleza de las cuentas
NATURALEZA_DEUDORA = "Deudora"
NATURALEZA_ACREEDORA = "Acreedora"

# Tipos de transacción
TIPO_TRANSACCION_VENTA = "Venta"
TIPO_TRANSACCION_COMPRA = "Compra"
TIPO_TRANSACCION_GENERAL = "General"

# Tipos de actividad para auditoría
ACTIVIDAD_LOGIN = "Login"
ACTIVIDAD_LOGOUT = "Logout"
ACTIVIDAD_CREAR_USUARIO = "Crear Usuario"
ACTIVIDAD_CREAR_TRANSACCION = "Crear Transacción"
ACTIVIDAD_VENTA = "Registrar Venta"
ACTIVIDAD_COMPRA = "Registrar Compra"
ACTIVIDAD_CERRAR_PERIODO = "Cerrar Período"
