import mysql.connector
from mysql.connector import Error

try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",       
            password="ivhs2210"        
        )

        if conexion.is_connected():
              print("Conexion exitosa")

except Error as e:
        print(f"Error: {e}")
finally:
      if conexion.is_connected():
        conexion.close()