import sqlite3
from datetime import datetime, timezone
import time
import random
import requests

class servicio():

    def __init__(self, nombre_servicio, servicios, mensajes):
        self.nombre_servicio = nombre_servicio
        self.servicios = servicios
        self.mensajes = mensajes
        self.severidades = ["INFO","WARNING","ERROR"]
 

    def creacion_logs(self):
        # ---- combinaciones ----
        log = {
            "timestamp" : datetime.now(timezone.utc).isoformat(),
            "service" : random.choice(self.servicios),
            "severity" : random.choice(self.severidades),
            "message" : random.choice(self.mensajes)
        }
        return log

    def envio_log(self, cantidad, url_server):

        for i in range(cantidad):
            log = self.creacion_logs()

            try: 
                response = requests.post(url_server, json=log, headers={"Authorization" : "XYZ123"})
                if response.status_code == 200:
                    print("se logro enviar")
                else:
                    print("no se logro enviar")
            except Exception as e:
                print(f"Error de conexion {e}")
            
            time.sleep(1)

def revisar_log(datos):
    contenido_json = [
        "timestamp", 
        "service", 
        "severity",
        "message"
        ]

    for elemento in contenido_json:
        if elemento not in datos:
            return False, f"el campo {elemento} no se encuetra en los datos enviados"
    
    try:
        datetime.fromisoformat(datos["timestamp"].replace("Z", "+00:00"))
    except ValueError:
        return False, "[timestamp] : invalido"
    
    if datos["severity"] not in ["INFO","WARNING","ERROR"]:
        return False, "[severity] : invalido"
    
    return True, "[status] : OK"



def guardar_log(datos):
    conexion = sqlite3.connect("data_base_logs.db")
    cursor = conexion.cursor()

    cursor.execute("""
    INSERT INTO ServiceLogs(timestamp, service, severity, message, received_at)
    VALUES (?, ?, ?, ?, ?)""", (
        datos["timestamp"], 
        datos["service"], 
        datos["severity"], 
        datos["message"], 
        datetime.now(timezone.utc).isoformat()
    ))

    conexion.commit()
    return cursor.lastrowid