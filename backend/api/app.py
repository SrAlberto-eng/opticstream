from flask import Flask, request
from flask_restful import Api, Resource

opticstream = Flask(__name__)
api = Api(opticstream)

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