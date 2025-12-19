
import time

class DetectorCambios:
    def __init__(self):
        self.estado_anterior = {"track_ids": set(), "clases": {}}

    def detectar_cambios(self, predicciones):
        track_ids_actuales = set(p["track_id"] for p in predicciones if p["track_id"])
        clases_actuales = {}
        for p in predicciones:
            clase = p["class_name"]
            clases_actuales[clase] = clases_actuales.get(clase, 0) + 1

        
        nuevos = track_ids_actuales - self.estado_anterior["track_ids"]
        salieron = self.estado_anterior["track_ids"] - track_ids_actuales
        cambio_clases = clases_actuales != self.estado_anterior["clases"]


        hay_cambio = bool(nuevos or salieron or cambio_clases)

        evento = None
        if hay_cambio:
            evento = {
                "timestamp": time.time(),
                "nuevos_ids": list(nuevos),
                "ids_salieron": list(salieron),
                "total_objetos": len(predicciones),
                "conteo_clases": clases_actuales,
                "predicciones": predicciones
            }

        self.estado_anterior["track_ids"] = track_ids_actuales
        self.estado_anterior["clases"] = clases_actuales

        return hay_cambio, evento