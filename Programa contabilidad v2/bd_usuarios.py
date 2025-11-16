import json
import os
from usuarios import Usuario

# Obtener la ruta del directorio donde está este script
DIRECTORIO_SCRIPT = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_USUARIOS = os.path.join(DIRECTORIO_SCRIPT, "usuarios.json")

def guardar_usuarios(sistema_usuarios):
    """Guarda todos los usuarios en el archivo JSON"""
    datos_usuarios = {}
    
    for username, usuario in sistema_usuarios.usuarios.items():
        datos_usuarios[username] = {
            "username": usuario.username,
            "password_hash": usuario.password_hash,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "documento": usuario.documento,
            "nivel": usuario.nivel,
            "fecha_creacion": usuario.fecha_creacion
        }
    
    with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(datos_usuarios, f, indent=4, ensure_ascii=False)

def cargar_usuarios(sistema_usuarios):
    """Carga los usuarios desde el archivo JSON"""
    if not os.path.exists(ARCHIVO_USUARIOS) or os.path.getsize(ARCHIVO_USUARIOS) == 0:
        return  # No hacer nada si no existe o está vacío

    try:
        with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
            datos_usuarios = json.load(f)
        
        # Limpiar usuarios existentes (excepto el admin por defecto si no está en el archivo)
        sistema_usuarios.usuarios.clear()
        
        # Recrear usuarios desde los datos guardados
        for username, datos in datos_usuarios.items():
            usuario = Usuario.__new__(Usuario)  # Crear instancia sin llamar __init__
            usuario.username = datos["username"]
            usuario.password_hash = datos["password_hash"]  # Ya está hasheada
            usuario.nombre = datos["nombre"]
            usuario.apellido = datos["apellido"]
            usuario.documento = datos["documento"]
            usuario.nivel = datos["nivel"]
            usuario.fecha_creacion = datos["fecha_creacion"]
            
            sistema_usuarios.usuarios[username] = usuario
            
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error al cargar usuarios: {e}")
        return  # No hacer nada si hay error en el archivo

def guardar_actividades(sistema_usuarios):
    """Guarda el log de actividades en un archivo separado"""
    archivo_actividades = os.path.join(DIRECTORIO_SCRIPT, "log_actividades.json")
    
    with open(archivo_actividades, "w", encoding="utf-8") as f:
        json.dump(sistema_usuarios.log_actividades, f, indent=4, ensure_ascii=False)

def cargar_actividades(sistema_usuarios):
    """Carga el log de actividades desde el archivo"""
    archivo_actividades = os.path.join(DIRECTORIO_SCRIPT, "log_actividades.json")
    
    if not os.path.exists(archivo_actividades) or os.path.getsize(archivo_actividades) == 0:
        return  # No hacer nada si no existe o está vacío

    try:
        with open(archivo_actividades, "r", encoding="utf-8") as f:
            sistema_usuarios.log_actividades = json.load(f)
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error al cargar actividades: {e}")
        sistema_usuarios.log_actividades = []  # Reiniciar si hay error

def inicializar_usuarios(sistema_usuarios):
    """Carga usuarios y actividades al inicializar el sistema"""
    cargar_usuarios(sistema_usuarios)
    cargar_actividades(sistema_usuarios)