from flask import Flask
from flask_restful import Api

opticstream = Flask(__name__)
api = Api(opticstream)

from routes.streams import StreamList, StreamIniciar, StreamDetener, StreamActivo
from routes.detecciones import DeteccionList, DeteccionDetail, ObjetosByDeteccion

api.add_resource(StreamList, "/streams")
api.add_resource(StreamIniciar, "/stream/iniciar")
api.add_resource(StreamDetener, "/stream/<int:stream_id>/detener")
api.add_resource(StreamActivo, "/stream/activo")

api.add_resource(DeteccionList, "/detecciones", "/detecciones/<int:stream_id>")
api.add_resource(DeteccionDetail, "/deteccion/<int:deteccion_id>")
api.add_resource(ObjetosByDeteccion, "/deteccion/<int:deteccion_id>/objetos")

@opticstream.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    opticstream.run(debug=True, port=5000)