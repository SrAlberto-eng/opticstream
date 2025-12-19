"""
Rutas para gestión de streams (sesiones de detección)
"""
from flask import request
from flask_restful import Resource
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.repository import (
    crear_stream, 
    cerrar_stream, 
    obtener_stream_activo,
    obtener_streams
)


class StreamList(Resource):
    """GET /streams - Lista todos los streams"""
    def get(self):
        limite = request.args.get('limite', 50, type=int)
        streams = obtener_streams(limite)
        return {"streams": streams}


class StreamIniciar(Resource):
    """POST /stream/iniciar - Inicia una nueva sesión"""
    def post(self):
        data = request.get_json() or {}
        nombre = data.get('nombre', 'Stream')
        fuente = data.get('fuente', '0')
        
        stream_id = crear_stream(nombre, fuente)
        
        if stream_id:
            return {"stream_id": stream_id, "mensaje": "Stream iniciado"}, 201
        else:
            return {"error": "No se pudo crear el stream"}, 500


class StreamDetener(Resource):
    """POST /stream/<stream_id>/detener - Detiene un stream"""
    def post(self, stream_id):
        if cerrar_stream(stream_id):
            return {"mensaje": f"Stream {stream_id} cerrado"}
        else:
            return {"error": "No se pudo cerrar el stream"}, 500


class StreamActivo(Resource):
    """GET /stream/activo - Obtiene el stream activo"""
    def get(self):
        stream = obtener_stream_activo()
        if stream:
            return {"stream": stream}
        else:
            return {"mensaje": "No hay stream activo"}, 404
