"""
Punto de entrada principal de la aplicación ContabilidadPro
"""
import sys
# Importamos Path de pathlib
from pathlib import Path 
from PyQt6.QtWidgets import QApplication
from app.core.database import init_db, get_session
from app.services.auth_service import AuthService
from app.gui.views.login_view import LoginView
from app.gui.main_window import MainWindow
from app.utils.logger import app_logger
# Importamos config
import config


def main():
    """Función principal de la aplicación"""
    try:
        # Inicializar base de datos
        app_logger.info("Inicializando base de datos...")
        init_db()
        
        # Crear usuario admin por defecto
        with get_session() as session:
            auth_service = AuthService(session)
            auth_service.crear_admin_default()
            app_logger.info("Usuario administrador verificado")
        
        # Crear aplicación Qt
        app = QApplication(sys.argv)
        app.setApplicationName("ContabilidadPro")
        app.setOrganizationName("ContabilidadPro")
        
        # --- INICIO DEL CAMBIO: Cargar Estilos ---
        
        # Construir la ruta al archivo QSS
        qss_file = config.BASE_DIR / "app" / "gui" / "styles" / "custom_styles.qss"
        
        try:
            with open(qss_file, "r") as f:
                app.setStyleSheet(f.read())
                app_logger.info("Estilo QSS cargado exitosamente.")
        except FileNotFoundError:
            app_logger.warning("No se encontró el archivo custom_styles.qss. Usando estilo por defecto.")
        except Exception as e:
            app_logger.error(f"Error al cargar QSS: {e}")
            
        # --- FIN DEL CAMBIO ---

        # Mostrar login
        login_window = LoginView()
        
        if not login_window.exec() or not login_window.usuario_autenticado:
            app_logger.info("Login cancelado o fallido. Saliendo.")
            sys.exit(0)  
        
        usuario = login_window.usuario_autenticado
        app_logger.info(f"Usuario {usuario.username} autenticado exitosamente")
        
        main_window = MainWindow(usuario)
        main_window.show()
        
        sys.exit(app.exec())
            
    except Exception as e:
        app_logger.error(f"Error fatal al iniciar la aplicación: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()