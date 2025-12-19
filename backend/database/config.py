import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME", "opticstream")
}

def conectar():
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def cerrar(conexion):
    if conexion and conexion.is_connected():
        conexion.close()
