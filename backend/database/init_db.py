
import mysql.connector
from mysql.connector import Error

def crear_base_de_datos():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",       
            password="ivhs2210"  
        )
        
        if conexion.is_connected():
            cursor = conexion.cursor()
            
            cursor.execute("CREATE DATABASE IF NOT EXISTS opticstream")
            print("Base de datos 'opticstream' creada")
            
            cursor.execute("USE opticstream")
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS streams (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    nombre VARCHAR(100) NOT NULL,
                    fuente VARCHAR(255) NOT NULL,
                    inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
                    fin DATETIME NULL,
                    activo BOOLEAN DEFAULT TRUE
                )
            """)
            print("Tabla 'streams' creada")
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS detecciones (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    stream_id INT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    total_objetos INT DEFAULT 0,
                    tipo_evento VARCHAR(50),
                    FOREIGN KEY (stream_id) REFERENCES streams(id) ON DELETE CASCADE
                )
            """)
            print("Tabla 'detecciones' creada")
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS objetos (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    deteccion_id INT NOT NULL,
                    track_id INT NULL,
                    class_id INT NOT NULL,
                    class_name VARCHAR(50) NOT NULL,
                    confidence FLOAT NOT NULL,
                    FOREIGN KEY (deteccion_id) REFERENCES detecciones(id) ON DELETE CASCADE
                )
            """)
            print("Tabla 'objetos' creada")
            
            try:
                cursor.execute("CREATE INDEX idx_detecciones_stream ON detecciones(stream_id)")
                cursor.execute("CREATE INDEX idx_detecciones_timestamp ON detecciones(timestamp)")
                cursor.execute("CREATE INDEX idx_objetos_deteccion ON objetos(deteccion_id)")
                cursor.execute("CREATE INDEX idx_objetos_class ON objetos(class_name)")
                print("Índices creados")
            except Error:
                print("Índices ya existen")
            
            conexion.commit()
            print("\nBase de datos inicializada correctamente")
            
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

if __name__ == "__main__":
    crear_base_de_datos()
