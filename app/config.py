"""
Este módulo carga las variables de entorno desde un archivo .env y configura la base de datos
para una aplicación Flask utilizando SQLAlchemy.
"""

import os  # Módulo estándar de Python para interactuar con el sistema operativo
from dotenv import load_dotenv  # Cargar variables de entorno desde un archivo .env

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Crear una clase para manejar las configuraciones del proyecto
class Config:
    """
    Clase de configuración para la aplicación Flask.
    Utiliza var cargadas desde el archivo .env para configurar la URI de la base de datos.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # Obtener la URL de  .env
