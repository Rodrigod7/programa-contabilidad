import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
from contabilidad import Contabilidad
from login import LoginWindow
from bd_contabilidad import guardar_datos

class ContabilidadGUI:
    def __init__(self):
        self.contabilidad = Contabilidad()

        # Login
        self.root = tk.Tk()
        self.root.withdraw()
        login = LoginWindow(self.contabilidad)
        self.root.wait_window(login.root)

        if not login.resultado:
            self.root.destroy()
            return

        self.root.deiconify()
        usuario = self.contabilidad.sistema_usuarios.usuario_actual
        self.root.title(f"Contabilidad - {usuario.nombre} {usuario.apellido}")
        self.root.geometry("900x700")

        self.crear_interfaz()

    def crear_interfaz(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        nivel = self.contabilidad.sistema_usuarios.usuario_actual.nivel

        if nivel == 1:
            # Solo pestaña de ventas y compras para trabajadores
            self.frame_ventas_compras = ttk.Frame(notebook)
            notebook.add(self.frame_ventas_compras, text="Ventas y Compras")
            self.crear_pestaña_ventas_compras()
        else:
            # Todas las pestañas para administradores
            pestañas_config = [
                ("frame_registro", "Registro", self.crear_pestaña_registro),
                ("frame_activo", "Activo", self.crear_pestaña_activo),
                ("frame_pasivo", "Pasivo", self.crear_pestaña_pasivo),
                ("frame_patrimonio", "Patrimonio Neto", self.crear_pestaña_patrimonio),
                ("frame_resultados", "Resultados", self.crear_pestaña_resultados),
                ("frame_balance", "Balance", self.crear_pestaña_balance),
                ("frame_usuarios", "Usuarios", self.crear_pestaña_usuarios),
                ("frame_monitoreo", "Monitoreo", self.crear_pestaña_monitoreo),
            ]

            for frame_attr, nombre, metodo in pestañas_config:
                frame = ttk.Frame(notebook)
                setattr(self, frame_attr, frame)
                notebook.add(frame, text=nombre)
                metodo()

        # Botón cerrar sesión
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill='x', padx=10, pady=5)
        ttk.Button(btn_frame, text="Cerrar Sesión", command=self.cerrar_sesion).pack(side='right')

    def crear_pestaña_ventas_compras(self):
        """Pestaña simplificada para trabajadores nivel 1"""
        main = ttk.Frame(self.frame_ventas_compras)
        main.pack(fill='both', expand=True, padx=20, pady=20)

        ttk.Label(main, text="Registro de Ventas y Compras", font=('Arial', 14, 'bold')).pack(pady=10)

        # Frame para ventas
        frame_venta = ttk.LabelFrame(main, text="Registrar Venta")
        frame_venta.pack(fill='x', pady=10)
        
        self.venta_concepto = tk.StringVar()
        self.venta_monto = tk.StringVar()
        
        ttk.Label(frame_venta, text="Concepto:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        ttk.Entry(frame_venta, textvariable=self.venta_concepto, width=30).grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(frame_venta, text="Monto ($):").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        ttk.Entry(frame_venta, textvariable=self.venta_monto, width=30).grid(row=1, column=1, padx=10, pady=5)
        ttk.Button(frame_venta, text="Registrar Venta", command=self.registrar_venta).grid(row=2, column=0, columnspan=2, pady=10)

        # Frame para compras
        frame_compra = ttk.LabelFrame(main, text="Registrar Compra")
        frame_compra.pack(fill='x', pady=10)
        
        self.compra_concepto = tk.StringVar()
        self.compra_monto = tk.StringVar()
        
        ttk.Label(frame_compra, text="Concepto:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        ttk.Entry(frame_compra, textvariable=self.compra_concepto, width=30).grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(frame_compra, text="Monto ($):").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        ttk.Entry(frame_compra, textvariable=self.compra_monto, width=30).grid(row=1, column=1, padx=10, pady=5)
        ttk.Button(frame_compra, text="Registrar Compra", command=self.registrar_compra).grid(row=2, column=0, columnspan=2, pady=10)

    def crear_pestaña_registro(self):
        """Pestaña de registro general para administradores"""
        main = ttk.Frame(self.frame_registro)
        main.pack(fill='both', expand=True, padx=20, pady=20)

        ttk.Label(main, text="Registro de Transacciones", font=('Arial', 14, 'bold')).pack(pady=10)

        # Formulario
        form_frame = ttk.LabelFrame(main, text="Nueva Transacción")
        form_frame.pack(fill='x', pady=10)

        # Variables del formulario
        self.tipo_var = tk.StringVar()
        self.concepto_var = tk.StringVar()
        self.monto_var = tk.StringVar()

        # Tipo de transacción
        ttk.Label(form_frame, text="Tipo:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
        tipo_combo = ttk.Combobox(form_frame, textvariable=self.tipo_var, width=25)
        tipo_combo['values'] = ('Activo Corriente', 'Activo No Corriente', 
                               'Pasivo Corriente', 'Pasivo No Corriente',
                               'Capital', 'Reservas', 'Ingreso', 'Gasto')
        tipo_combo.grid(row=0, column=1, padx=10, pady=5)

        # Concepto
        ttk.Label(form_frame, text="Concepto/Cuenta:").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.concepto_var, width=30).grid(row=1, column=1, padx=10, pady=5)

        # Monto
        ttk.Label(form_frame, text="Monto ($):").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.monto_var, width=30).grid(row=2, column=1, padx=10, pady=5)

        # Botones
        ttk.Button(form_frame, text="Registrar", command=self.registrar_transaccion).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(main, text="Cerrar Período", command=self.cerrar_periodo).pack(pady=10)

    def crear_pestaña_con_texto(self, frame, titulo, metodo_actualizar):
        """Método auxiliar para crear pestañas con área de texto"""
        text_widget = scrolledtext.ScrolledText(frame, height=30, width=80)
        text_widget.pack(padx=20, pady=20, fill='both', expand=True)
        
        btn_actualizar = ttk.Button(frame, text=f"Actualizar {titulo}", command=metodo_actualizar)
        btn_actualizar.pack(pady=10)
        
        return text_widget

    def crear_pestaña_activo(self):
        self.activo_text = self.crear_pestaña_con_texto(self.frame_activo, "Activo", self.actualizar_activo)

    def crear_pestaña_pasivo(self):
        self.pasivo_text = self.crear_pestaña_con_texto(self.frame_pasivo, "Pasivo", self.actualizar_pasivo)

    def crear_pestaña_patrimonio(self):
        self.patrimonio_text = self.crear_pestaña_con_texto(self.frame_patrimonio, "Patrimonio", self.actualizar_patrimonio)

    def crear_pestaña_resultados(self):
        self.resultados_text = self.crear_pestaña_con_texto(self.frame_resultados, "Resultados", self.actualizar_resultados)

    def crear_pestaña_balance(self):
        self.balance_text = self.crear_pestaña_con_texto(self.frame_balance, "Balance", self.actualizar_balance)

    def crear_pestaña_usuarios(self):
        """Gestión de usuarios (solo administradores)"""
        main = ttk.Frame(self.frame_usuarios)
        main.pack(fill='both', expand=True, padx=20, pady=20)

        ttk.Label(main, text="Gestión de Usuarios", font=('Arial', 14, 'bold')).pack(pady=10)

        # Formulario para crear usuario
        crear_frame = ttk.LabelFrame(main, text="Crear Nuevo Usuario")
        crear_frame.pack(fill='x', pady=10)

        # Variables para nuevo usuario
        campos_usuario = [
            ("Usuario:", "new_username_var"),
            ("Contraseña:", "new_password_var"),
            ("Nombre:", "new_nombre_var"),
            ("Apellido:", "new_apellido_var"),
            ("Documento:", "new_documento_var")
        ]

        for i, (label, var_name) in enumerate(campos_usuario):
            ttk.Label(crear_frame, text=label).grid(row=i, column=0, sticky='w', padx=10, pady=5)
            var = tk.StringVar()
            setattr(self, var_name, var)
            show = "*" if "password" in var_name else None
            ttk.Entry(crear_frame, textvariable=var, show=show).grid(row=i, column=1, padx=10, pady=5)

        # Nivel de usuario
        ttk.Label(crear_frame, text="Nivel:").grid(row=5, column=0, sticky='w', padx=10, pady=5)
        self.new_nivel_var = tk.StringVar()
        nivel_combo = ttk.Combobox(crear_frame, textvariable=self.new_nivel_var)
        nivel_combo['values'] = ('1 - Trabajador', '2 - Administrador')
        nivel_combo.grid(row=5, column=1, padx=10, pady=5)

        ttk.Button(crear_frame, text="Crear Usuario", command=self.crear_usuario).grid(row=6, column=0, columnspan=2, pady=10)

        # Lista de usuarios
        lista_frame = ttk.LabelFrame(main, text="Usuarios Registrados")
        lista_frame.pack(fill='both', expand=True, pady=10)

        self.usuarios_text = scrolledtext.ScrolledText(lista_frame, height=15)
        self.usuarios_text.pack(fill='both', expand=True, padx=10, pady=10)

        ttk.Button(lista_frame, text="Actualizar Lista", command=self.actualizar_usuarios).pack(pady=5)

    def crear_pestaña_monitoreo(self):
        """Monitoreo de actividades (solo administradores)"""
        main = ttk.Frame(self.frame_monitoreo)
        main.pack(fill='both', expand=True, padx=20, pady=20)

        ttk.Label(main, text="Monitoreo de Actividades", font=('Arial', 14, 'bold')).pack(pady=10)

        # Filtros
        filtro_frame = ttk.LabelFrame(main, text="Filtros")
        filtro_frame.pack(fill='x', pady=10)

        ttk.Label(filtro_frame, text="Usuario:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.filtro_usuario_var = tk.StringVar()
        self.filtro_usuario_combo = ttk.Combobox(filtro_frame, textvariable=self.filtro_usuario_var)
        self.filtro_usuario_combo.grid(row=0, column=1, padx=10, pady=5)

        ttk.Button(filtro_frame, text="Filtrar", command=self.filtrar_actividades).grid(row=0, column=2, padx=10)
        ttk.Button(filtro_frame, text="Mostrar Todo", command=self.mostrar_todas_actividades).grid(row=0, column=3, padx=10)

        # Log de actividades
        self.actividades_text = scrolledtext.ScrolledText(main, height=25)
        self.actividades_text.pack(fill='both', expand=True, pady=10)

    # === MÉTODOS DE REGISTRO ===
    def registrar_venta(self):
        self._registrar_operacion(self.venta_concepto, self.venta_monto, self.contabilidad.agregar_venta, "Venta")

    def registrar_compra(self):
        self._registrar_operacion(self.compra_concepto, self.compra_monto, self.contabilidad.agregar_compra, "Compra")

    def _registrar_operacion(self, concepto_var, monto_var, metodo_registro, tipo_operacion):
        """Método auxiliar para registrar operaciones"""
        try:
            concepto = concepto_var.get().strip()
            monto = float(monto_var.get())
            
            if not concepto or monto <= 0:
                raise ValueError("Datos inválidos")
            
            metodo_registro(concepto, monto)
            messagebox.showinfo("Éxito", f"{tipo_operacion} registrada: {concepto} - ${monto:,.2f}")
            
            # Limpiar campos
            concepto_var.set("")
            monto_var.set("")
            
        except ValueError:
            messagebox.showerror("Error", "Complete correctamente los campos")

    def registrar_transaccion(self):
        """Registrar transacción general (administradores)"""
        try:
            tipo = self.tipo_var.get()
            concepto = self.concepto_var.get().strip()
            monto = float(self.monto_var.get())

            if not tipo or not concepto or monto <= 0:
                messagebox.showerror("Error", "Todos los campos son obligatorios y el monto debe ser positivo")
                return

            # Mapeo de tipos a métodos
            tipos_metodos = {
                "Activo Corriente": lambda: self.contabilidad.agregar_activo_corriente(concepto, monto),
                "Activo No Corriente": lambda: self.contabilidad.agregar_activo_no_corriente(concepto, monto),
                "Pasivo Corriente": lambda: self.contabilidad.agregar_pasivo_corriente(concepto, monto),
                "Pasivo No Corriente": lambda: self.contabilidad.agregar_pasivo_no_corriente(concepto, monto),
                "Capital": lambda: self.contabilidad.establecer_capital(monto),
                "Reservas": lambda: self.contabilidad.agregar_reservas(monto),
                "Ingreso": lambda: self.contabilidad.agregar_ingreso(concepto, monto),
                "Gasto": lambda: self.contabilidad.agregar_gasto(concepto, monto)
            }

            if tipo in tipos_metodos:
                tipos_metodos[tipo]()
                messagebox.showinfo("Éxito", f"{tipo} registrado correctamente:\n{concepto}: ${monto:,.2f}")
                guardar_datos(self.contabilidad)

                # Limpiar campos
                self.concepto_var.set("")
                self.monto_var.set("")

        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido")
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar: {str(e)}")

    # === MÉTODOS DE ACTUALIZACIÓN ===
    def actualizar_activo(self):
        self._actualizar_cuentas(self.activo_text, "ACTIVO", [
            ("ACTIVO CORRIENTE", self.contabilidad.activo_corriente),
            ("ACTIVO NO CORRIENTE", self.contabilidad.activo_no_corriente)
        ])

    def actualizar_pasivo(self):
        self._actualizar_cuentas(self.pasivo_text, "PASIVO", [
            ("PASIVO CORRIENTE", self.contabilidad.pasivo_corriente),
            ("PASIVO NO CORRIENTE", self.contabilidad.pasivo_no_corriente)
        ])

    def _actualizar_cuentas(self, text_widget, titulo, secciones):
        """Método auxiliar para actualizar cuentas"""
        text_widget.delete(1.0, tk.END)
        
        contenido = f"{'=' * 50}\n{titulo}\n{'=' * 50}\n\n"
        total_general = 0
        
        for nombre_seccion, cuentas in secciones:
            contenido += f"{nombre_seccion}:\n"
            total_seccion = sum(cuentas.values())
            
            for cuenta, monto in cuentas.items():
                contenido += f"  {cuenta}: ${monto:,.2f}\n"
            
            contenido += f"  TOTAL {nombre_seccion}: ${total_seccion:,.2f}\n\n"
            total_general += total_seccion
        
        contenido += f"TOTAL {titulo}: ${total_general:,.2f}\n"
        text_widget.insert(1.0, contenido)

    def actualizar_patrimonio(self):
        self.patrimonio_text.delete(1.0, tk.END)
        
        resultado_periodo = self.contabilidad.calcular_resultado_periodo()
        total_patrimonio = self.contabilidad.calcular_patrimonio_neto()
        
        contenido = f"{'=' * 50}\nPATRIMONIO NETO\n{'=' * 50}\n\n"
        contenido += f"Capital: ${self.contabilidad.capital:,.2f}\n"
        contenido += f"Reservas: ${self.contabilidad.reservas:,.2f}\n"
        contenido += f"Resultados Acumulados: ${self.contabilidad.resultados_acumulados:,.2f}\n"
        contenido += f"Resultado del Período: ${resultado_periodo:,.2f}\n\n"
        contenido += f"TOTAL PATRIMONIO NETO: ${total_patrimonio:,.2f}\n"
        
        self.patrimonio_text.insert(1.0, contenido)

    def actualizar_resultados(self):
        self.resultados_text.delete(1.0, tk.END)
        
        total_ingresos = sum(self.contabilidad.ingresos.values())
        total_gastos = sum(self.contabilidad.gastos.values())
        resultado = total_ingresos - total_gastos
        
        contenido = f"{'=' * 50}\nESTADO DE RESULTADOS\n{'=' * 50}\n\n"
        
        contenido += "INGRESOS:\n"
        for concepto, monto in self.contabilidad.ingresos.items():
            contenido += f"  {concepto}: ${monto:,.2f}\n"
        contenido += f"  TOTAL INGRESOS: ${total_ingresos:,.2f}\n\n"
        
        contenido += "GASTOS:\n"
        for concepto, monto in self.contabilidad.gastos.items():
            contenido += f"  {concepto}: ${monto:,.2f}\n"
        contenido += f"  TOTAL GASTOS: ${total_gastos:,.2f}\n\n"
        
        contenido += f"RESULTADO DEL PERÍODO: ${resultado:,.2f}\n"
        contenido += f"({'GANANCIA' if resultado > 0 else 'PÉRDIDA' if resultado < 0 else 'PUNTO DE EQUILIBRIO'})\n"
        
        self.resultados_text.insert(1.0, contenido)

    def actualizar_balance(self):
        self.balance_text.delete(1.0, tk.END)
        
        # Calcular totales
        total_activo_corriente = sum(self.contabilidad.activo_corriente.values())
        total_activo_no_corriente = sum(self.contabilidad.activo_no_corriente.values())
        total_activo = total_activo_corriente + total_activo_no_corriente
        
        total_pasivo_corriente = sum(self.contabilidad.pasivo_corriente.values())
        total_pasivo_no_corriente = sum(self.contabilidad.pasivo_no_corriente.values())
        total_pasivo = total_pasivo_corriente + total_pasivo_no_corriente
        
        total_patrimonio = self.contabilidad.calcular_patrimonio_neto()
        resultado_periodo = self.contabilidad.calcular_resultado_periodo()
        
        contenido = f"{'=' * 60}\nBALANCE GENERAL\n"
        contenido += f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n{'=' * 60}\n\n"
        
        # ACTIVO
        contenido += f"ACTIVO\n{'-' * 30}\n"
        contenido += "ACTIVO CORRIENTE:\n"
        for cuenta, monto in self.contabilidad.activo_corriente.items():
            contenido += f"  {cuenta}: ${monto:,.2f}\n"
        contenido += f"  TOTAL ACTIVO CORRIENTE: ${total_activo_corriente:,.2f}\n\n"
        
        contenido += "ACTIVO NO CORRIENTE:\n"
        for cuenta, monto in self.contabilidad.activo_no_corriente.items():
            contenido += f"  {cuenta}: ${monto:,.2f}\n"
        contenido += f"  TOTAL ACTIVO NO CORRIENTE: ${total_activo_no_corriente:,.2f}\n\n"
        contenido += f"TOTAL ACTIVO: ${total_activo:,.2f}\n\n"
        
        # PASIVO
        contenido += f"PASIVO\n{'-' * 30}\n"
        contenido += "PASIVO CORRIENTE:\n"
        for cuenta, monto in self.contabilidad.pasivo_corriente.items():
            contenido += f"  {cuenta}: ${monto:,.2f}\n"
        contenido += f"  TOTAL PASIVO CORRIENTE: ${total_pasivo_corriente:,.2f}\n\n"
        
        contenido += "PASIVO NO CORRIENTE:\n"
        for cuenta, monto in self.contabilidad.pasivo_no_corriente.items():
            contenido += f"  {cuenta}: ${monto:,.2f}\n"
        contenido += f"  TOTAL PASIVO NO CORRIENTE: ${total_pasivo_no_corriente:,.2f}\n\n"
        contenido += f"TOTAL PASIVO: ${total_pasivo:,.2f}\n\n"
        
        # PATRIMONIO NETO
        contenido += f"PATRIMONIO NETO\n{'-' * 30}\n"
        contenido += f"Capital: ${self.contabilidad.capital:,.2f}\n"
        contenido += f"Reservas: ${self.contabilidad.reservas:,.2f}\n"
        contenido += f"Resultados Acumulados: ${self.contabilidad.resultados_acumulados:,.2f}\n"
        contenido += f"Resultado del Período: ${resultado_periodo:,.2f}\n"
        contenido += f"TOTAL PATRIMONIO NETO: ${total_patrimonio:,.2f}\n\n"
        
        # VERIFICACIÓN
        contenido += f"{'=' * 60}\nVERIFICACIÓN ECUACIÓN CONTABLE\n{'=' * 60}\n"
        contenido += f"ACTIVO: ${total_activo:,.2f}\n"
        contenido += f"PASIVO + PATRIMONIO NETO: ${total_pasivo + total_patrimonio:,.2f}\n"
        
        if abs(total_activo - (total_pasivo + total_patrimonio)) < 0.01:
            contenido += "✓ La ecuación contable está balanceada\n"
        else:
            contenido += "✗ ERROR: La ecuación contable NO está balanceada\n"
        
        self.balance_text.insert(1.0, contenido)

    # === MÉTODOS DE GESTIÓN DE USUARIOS ===
    def crear_usuario(self):
        try:
            campos = {
                'username': self.new_username_var.get().strip(),
                'password': self.new_password_var.get(),
                'nombre': self.new_nombre_var.get().strip(),
                'apellido': self.new_apellido_var.get().strip(),
                'documento': self.new_documento_var.get().strip(),
                'nivel_texto': self.new_nivel_var.get()
            }

            if not all(campos.values()):
                messagebox.showerror("Error", "Complete todos los campos")
                return

            nivel = int(campos['nivel_texto'].split(' - ')[0])
            
            exito, mensaje = self.contabilidad.sistema_usuarios.crear_usuario(
                campos['username'], campos['password'], campos['nombre'], 
                campos['apellido'], campos['documento'], nivel
            )

            if exito:
                messagebox.showinfo("Éxito", mensaje)
                # Limpiar campos
                for var_name in ['new_username_var', 'new_password_var', 'new_nombre_var', 
                               'new_apellido_var', 'new_documento_var', 'new_nivel_var']:
                    getattr(self, var_name).set("")
                self.actualizar_usuarios()
            else:
                messagebox.showerror("Error", mensaje)

        except Exception as e:
            messagebox.showerror("Error", f"Error al crear usuario: {str(e)}")

    def actualizar_usuarios(self):
        self.usuarios_text.delete(1.0, tk.END)
        
        contenido = f"USUARIOS REGISTRADOS\n{'=' * 50}\n\n"
        
        for username, usuario in self.contabilidad.sistema_usuarios.usuarios.items():
            nivel_texto = "Administrador" if usuario.nivel == 2 else "Trabajador"
            contenido += f"Usuario: {username}\n"
            contenido += f"Nombre: {usuario.nombre} {usuario.apellido}\n"
            contenido += f"Documento: {usuario.documento}\n"
            contenido += f"Nivel: {nivel_texto}\n"
            contenido += f"Creado: {usuario.fecha_creacion}\n"
            contenido += f"{'-' * 30}\n"
        
        self.usuarios_text.insert(1.0, contenido)
        
        # Actualizar combo de usuarios para monitoreo
        usuarios = list(self.contabilidad.sistema_usuarios.usuarios.keys())
        self.filtro_usuario_combo['values'] = ['Todos'] + usuarios

    # === MÉTODOS DE MONITOREO ===
    def filtrar_actividades(self):
        usuario_filtro = self.filtro_usuario_var.get()
        self._mostrar_actividades(usuario_filtro)

    def mostrar_todas_actividades(self):
        self.filtro_usuario_var.set("Todos")
        self._mostrar_actividades("Todos")

    def _mostrar_actividades(self, filtro):
        self.actividades_text.delete(1.0, tk.END)
        
        contenido = f"ACTIVIDADES - Filtro: {filtro}\n{'=' * 60}\n\n"
        
        for actividad in reversed(self.contabilidad.sistema_usuarios.log_actividades):
            if filtro == "Todos" or actividad['usuario'] == filtro:
                contenido += f"Usuario: {actividad['usuario']} ({actividad['nombre_completo']})\n"
                contenido += f"Fecha/Hora: {actividad['fecha_hora']}\n"
                contenido += f"Actividad: {actividad['descripcion']}\n"
                contenido += f"{'-' * 50}\n"
        
        self.actividades_text.insert(1.0, contenido)

    # === MÉTODOS GENERALES ===
    def cerrar_periodo(self):
        resultado = self.contabilidad.cerrar_periodo()
        messagebox.showinfo("Período Cerrado", 
                           f"Período cerrado exitosamente.\n"
                           f"Resultado ${resultado:,.2f} transferido a Resultados Acumulados.\n"
                           f"Ingresos y Gastos reiniciados.")
        guardar_datos(self.contabilidad)

    def cerrar_sesion(self):
        self.contabilidad.sistema_usuarios.cerrar_sesion()
        self.root.destroy()

    def ejecutar(self):
        self.root.mainloop()