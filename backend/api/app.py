from flask import Flask, request
from flask_restful import Api, Resource
import json
import os

opticstream = Flask(__name__)
api = Api(opticstream)

@api.resource("/predicciones")
class Predicciones(Resource):
    def get(self):
        json_path = "modelo/temp/predictions.json"
        
        if not os.path.exists(json_path):
            return {"error": "No hay predicciones disponibles"}, 404
        
        try:
            with open(json_path, "r") as f:
                contenido = f.read()
                if not contenido.strip():
                    return {"predicciones": [], "mensaje": "Sin detecciones"}
                predicciones = json.loads(contenido)
        except json.JSONDecodeError:
            return {"error": "Error al leer predicciones"}, 500
        
        return {"predicciones": predicciones}

@api.resource("/prueba")
class Prueba(Resource):
    def get(self):
        return {"message": "GET"}
    
    def put(self):
        return {"message": "PUT"}

    def delete(self):
        return {"message": "DELETE"}
    
    def post(self):
        return {"message": "POST"}
    
    def patch(self):
        return {"message": "PATCH"}
    
    def head(self):
        return {"message": "HEAD"}
    
    def option(self):
        return {"message": "OPTION"}

#api.add_resource(Prueba, "/prueba")  

if __name__ == "__main__":
    opticstream.run(debug=True)