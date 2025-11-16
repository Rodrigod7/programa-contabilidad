import tkinter as tk
from tkinter import ttk, messagebox

class LoginWindow:
    def __init__(self, contabilidad):
        self.contabilidad = contabilidad
        self.root = tk.Toplevel()
        self.root.title("Iniciar Sesión")
        self.root.geometry("300x200")
        self.root.resizable(False, False)
        self.root.grab_set()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.resultado = False
        self.crear_interfaz()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def crear_interfaz(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        ttk.Label(main_frame, text="Sistema de Contabilidad", font=('Arial', 12, 'bold')).pack(pady=10)
        ttk.Label(main_frame, text="Usuario:").pack(anchor='w')
        ttk.Entry(main_frame, textvariable=self.username_var).pack(fill='x', pady=5)
        ttk.Label(main_frame, text="Contraseña:").pack(anchor='w')
        password_entry = ttk.Entry(main_frame, textvariable=self.password_var, show="*")
        password_entry.pack(fill='x', pady=5)
        password_entry.bind('<Return>', lambda e: self.login())
        ttk.Button(main_frame, text="Iniciar Sesión", command=self.login).pack(pady=10)
        info_frame = ttk.LabelFrame(main_frame, text="Acceso por defecto")
        info_frame.pack(fill='x', pady=10)
        ttk.Label(info_frame, text="Usuario: admin").pack()
        ttk.Label(info_frame, text="Contraseña: admin123").pack()

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        if not username or not password:
            messagebox.showerror("Error", "Complete todos los campos")
            return
        exito, mensaje = self.contabilidad.sistema_usuarios.autenticar(username, password)
        if exito:
            self.resultado = True
            self.root.destroy()
        else:
            messagebox.showerror("Error de Autenticación", mensaje)

    def on_closing(self):
        self.resultado = False
        self.root.destroy()
