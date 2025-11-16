from bd_contabilidad import guardar_datos, cargar_datos

class Contabilidad:
    def __init__(self):
        from usuarios import SistemaUsuarios
        self.sistema_usuarios = SistemaUsuarios()
        self.activo_corriente = {}
        self.activo_no_corriente = {}
        self.pasivo_corriente = {}
        self.pasivo_no_corriente = {}
        self.capital = 0
        self.reservas = 0
        self.resultados_acumulados = 0
        self.ingresos = {}
        self.gastos = {}
        # CARGAR DATOS AL INICIALIZAR
        cargar_datos(self)

    def agregar_venta(self, concepto, monto):
        self.agregar_ingreso(f"Venta: {concepto}", monto)
        if self.sistema_usuarios.usuario_actual:
            self.sistema_usuarios.registrar_actividad(f"Venta registrada: {concepto} - ${monto:,.2f}")
        guardar_datos(self)

    def agregar_compra(self, concepto, monto):
        self.agregar_gasto(f"Compra: {concepto}", monto)
        if self.sistema_usuarios.usuario_actual:
            self.sistema_usuarios.registrar_actividad(f"Compra registrada: {concepto} - ${monto:,.2f}")
        guardar_datos(self)
        
    def agregar_activo_corriente(self, cuenta, monto):
        self.activo_corriente[cuenta] = self.activo_corriente.get(cuenta, 0) + monto
        guardar_datos(self)

    def agregar_activo_no_corriente(self, cuenta, monto):
        self.activo_no_corriente[cuenta] = self.activo_no_corriente.get(cuenta, 0) + monto
        guardar_datos(self) 

    def agregar_pasivo_corriente(self, cuenta, monto):
        self.pasivo_corriente[cuenta] = self.pasivo_corriente.get(cuenta, 0) + monto
        guardar_datos(self)

    def agregar_pasivo_no_corriente(self, cuenta, monto):
        self.pasivo_no_corriente[cuenta] = self.pasivo_no_corriente.get(cuenta, 0) + monto
        guardar_datos(self)
   
    def establecer_capital(self, monto):
        self.capital = monto
        guardar_datos(self)

    def agregar_reservas(self, monto):
        self.reservas += monto
        guardar_datos(self)

    def agregar_ingreso(self, concepto, monto):
        self.ingresos[concepto] = self.ingresos.get(concepto, 0) + monto

    def agregar_gasto(self, concepto, monto):
        self.gastos[concepto] = self.gastos.get(concepto, 0) + monto

    def calcular_total_activo(self):
        return sum(self.activo_corriente.values()) + sum(self.activo_no_corriente.values())

    def calcular_total_pasivo(self):
        return sum(self.pasivo_corriente.values()) + sum(self.pasivo_no_corriente.values())

    def calcular_resultado_periodo(self):
        return sum(self.ingresos.values()) - sum(self.gastos.values())

    def calcular_patrimonio_neto(self):
        return self.capital + self.reservas + self.resultados_acumulados + self.calcular_resultado_periodo()

    def cerrar_periodo(self):
        resultado = self.calcular_resultado_periodo()
        self.resultados_acumulados += resultado
        self.ingresos.clear()
        self.gastos.clear()
        guardar_datos(self)
        return resultado
