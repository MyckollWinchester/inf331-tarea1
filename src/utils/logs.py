import logging

# Configuración básica de logging
logging.basicConfig(
    level=logging.INFO,  # Nivel mínimo de mensajes que se registrarán
    format='%(asctime)s %(levelname)s: %(message)s',  # Formato del mensaje
    datefmt='%d/%m/%Y %H:%M:%S',  # Formato de la fecha
    handlers=[
        logging.FileHandler("app.log"),  # Guardar logs en un archivo llamado "app.log"
    ]
)

# Crear un logger para usar en el proyecto
logger = logging.getLogger("AppLogger")