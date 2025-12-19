from datetime import datetime
from database.config import conectar, cerrar


# ============== STREAMS ==============

def crear_stream(nombre, fuente):
    """Crea una nueva sesión de detección"""
    conexion = conectar()
    if not conexion:
        return None
    
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO streams (nombre, fuente, activo) VALUES (%s, %s, %s)",
            (nombre, fuente, True)
        )
        conexion.commit()
        stream_id = cursor.lastrowid
        return stream_id
    except Exception as e:
        print(f"Error al crear stream: {e}")
        return None
    finally:
        cerrar(conexion)


def cerrar_stream(stream_id):
    """Cierra una sesión de detección"""
    conexion = conectar()
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE streams SET fin = %s, activo = %s WHERE id = %s",
            (datetime.now(), False, stream_id)
        )
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al cerrar stream: {e}")
        return False
    finally:
        cerrar(conexion)


def obtener_stream_activo():
    """Obtiene el stream activo actual"""
    conexion = conectar()
    if not conexion:
        return None
    
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM streams WHERE activo = TRUE LIMIT 1")
        return cursor.fetchone()
    except Exception as e:
        print(f"Error al obtener stream: {e}")
        return None
    finally:
        cerrar(conexion)


# ============== DETECCIONES ==============

def guardar_deteccion(stream_id, total_objetos, tipo_evento, predicciones):
    """
    Guarda una detección y sus objetos en la BD
    
    Args:
        stream_id: ID del stream activo
        total_objetos: Cantidad de objetos detectados
        tipo_evento: Tipo de evento ("entrada", "salida", "cambio")
        predicciones: Lista de diccionarios con los objetos detectados
    
    Returns:
        deteccion_id o None si falla
    """
    conexion = conectar()
    if not conexion:
        return None
    
    try:
        cursor = conexion.cursor()
        
        # Insertar detección
        cursor.execute(
            "INSERT INTO detecciones (stream_id, total_objetos, tipo_evento) VALUES (%s, %s, %s)",
            (stream_id, total_objetos, tipo_evento)
        )
        deteccion_id = cursor.lastrowid
        
        # Insertar cada objeto detectado
        for pred in predicciones:
            cursor.execute(
                """INSERT INTO objetos 
                   (deteccion_id, track_id, class_id, class_name, confidence, bbox_x, bbox_y, bbox_w, bbox_h) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    deteccion_id,
                    pred.get("track_id"),
                    pred.get("class_id"),
                    pred.get("class_name"),
                    pred.get("confidence"),
                    pred.get("bbox_x"),
                    pred.get("bbox_y"),
                    pred.get("bbox_w"),
                    pred.get("bbox_h")
                )
            )
        
        conexion.commit()
        return deteccion_id
    except Exception as e:
        print(f"Error al guardar detección: {e}")
        conexion.rollback()
        return None
    finally:
        cerrar(conexion)


def obtener_detecciones(stream_id=None, limite=100):
    """Obtiene las últimas detecciones"""
    conexion = conectar()
    if not conexion:
        return []
    
    try:
        cursor = conexion.cursor(dictionary=True)
        
        if stream_id:
            cursor.execute(
                """SELECT * FROM detecciones 
                   WHERE stream_id = %s 
                   ORDER BY timestamp DESC LIMIT %s""",
                (stream_id, limite)
            )
        else:
            cursor.execute(
                "SELECT * FROM detecciones ORDER BY timestamp DESC LIMIT %s",
                (limite,)
            )
        
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener detecciones: {e}")
        return []
    finally:
        cerrar(conexion)


def obtener_objetos_deteccion(deteccion_id):
    """Obtiene los objetos de una detección específica"""
    conexion = conectar()
    if not conexion:
        return []
    
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM objetos WHERE deteccion_id = %s",
            (deteccion_id,)
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener objetos: {e}")
        return []
    finally:
        cerrar(conexion)


def obtener_streams(limite=50):
    """Obtiene todos los streams"""
    conexion = conectar()
    if not conexion:
        return []
    
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM streams ORDER BY id DESC LIMIT %s",
            (limite,)
        )
        rows = cursor.fetchall()
        # Convertir datetime a string para JSON
        for row in rows:
            if row.get('inicio'):
                row['inicio'] = row['inicio'].isoformat()
            if row.get('fin'):
                row['fin'] = row['fin'].isoformat()
        return rows
    except Exception as e:
        print(f"Error al obtener streams: {e}")
        return []
    finally:
        cerrar(conexion)


def obtener_deteccion_con_objetos(deteccion_id):
    """Obtiene una detección con todos sus objetos"""
    conexion = conectar()
    if not conexion:
        return None
    
    try:
        cursor = conexion.cursor(dictionary=True)
        
        # Obtener detección
        cursor.execute(
            "SELECT * FROM detecciones WHERE id = %s",
            (deteccion_id,)
        )
        deteccion = cursor.fetchone()
        
        if not deteccion:
            return None
        
        # Convertir datetime
        if deteccion.get('timestamp'):
            deteccion['timestamp'] = deteccion['timestamp'].isoformat()
        
        # Obtener objetos
        cursor.execute(
            "SELECT * FROM objetos WHERE deteccion_id = %s",
            (deteccion_id,)
        )
        deteccion['objetos'] = cursor.fetchall()
        
        return deteccion
    except Exception as e:
        print(f"Error al obtener detección: {e}")
        return None
    finally:
        cerrar(conexion)
