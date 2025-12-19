from flask import request
from flask_restful import Resource
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.repository import (
    obtener_detecciones,
    obtener_objetos_deteccion,
    obtener_deteccion_con_objetos
)


class DeteccionList(Resource):
    """GET /detecciones - Lista las detecciones"""
    def get(self):
        stream_id = request.args.get('stream_id', type=int)
        limite = request.args.get('limite', 100, type=int)
        
        detecciones = obtener_detecciones(stream_id, limite)
        return {"detecciones": detecciones, "total": len(detecciones)}


class DeteccionDetail(Resource):
    """GET /detecciones/<id> - Detalle de una detección con sus objetos"""
    def get(self, deteccion_id):
        deteccion = obtener_deteccion_con_objetos(deteccion_id)
        
        if deteccion:
            return {"deteccion": deteccion}
        else:
            return {"error": "Detección no encontrada"}, 404


class ObjetosByDeteccion(Resource):
    """GET /detecciones/<id>/objetos - Objetos de una detección"""
    def get(self, deteccion_id):
        objetos = obtener_objetos_deteccion(deteccion_id)
        return {"objetos": objetos, "total": len(objetos)}
