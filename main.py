import paho.mqtt.client as mqtt
import csv
import json
from datetime import datetime

# Configuración del broker MQTT
host = "sensecap-openstream.seeed.cc"
port = 1883
username = "org-434181208382464"
password = "6552EBDADED14014B18359DB4C3B6D4B3984D0781C2545B6A33727A4BBA1E46E"
topic = "/device_sensor_data/434181208382464/2CF7F1C04430015D/1/vs/+"
client_id = "org-434181208382464-7"

# Los códigos que se quieren de los dispositivos
codigos = {
    "4097": "Air Temperature",
    "4098": "Air Humidity",
    "4099": "Light Intensity",
    "4101": "Barometric Pressure",
    "4104": "Wind Direction",
    "4105": "Wind Speed",
    "4113": "Rainfall Hourly",
    "4190": "UV Index"
}

# Nombre del archivo CSV y sus headers
csv_filename = "mediciones.csv"
csv_headers = ["Fecha", "Tipo de Medición", "Valor"]

def on_message(client, userdata, message):
    '''Método para almacenar las mediciones en un archivo CSV'''
    payload = str(message.payload.decode('utf-8'))

    # Obtener código del topic
    _, _, _, _, _, _, codigo = message.topic.split("/")

    # Verificar si el código está en la lista
    if codigo in codigos:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tipo_medicion = codigos[codigo]
        valor = json.loads(payload)["value"]

        # Escribir los datos en el archivo CSV
        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            # Verificar si el archivo está vacío para escribir los headers
            if file.tell() == 0:
                writer.writerow(csv_headers)
            writer.writerow([fecha, tipo_medicion, valor])
        print(f"Dato almacenado en el archivo CSV: Fecha: {fecha}, Tipo de Medición: {tipo_medicion}, Valor: {valor}")

# Configuración del cliente MQTT
client = mqtt.Client(client_id) # Corregido: Eliminada la versión de la API
client.username_pw_set(username, password)
client.on_message = on_message

# Conexión al broker
client.connect(host, port, 60)

# Suscripción al topic
client.subscribe(topic)

# Bucle principal para mantener la conexión y procesar mensajes
client.loop_forever()
