import requests

BASE = "http://127.0.0.1:5000/"

responde = requests.get(BASE + "prueba")
print(responde.json())