import paho.mqtt.client as mqtt
import json
import time

# Configuración del broker MQTT
BROKER = "localhost"  # Cambia esto según tu configuración
PORT = 1883
TOPIC = "incidencias/reporte"

# Reportes simulados de sensores
reports = [
    {
        "tipo": "Semáforo roto",
        "descripcion": "El semáforo no está funcionando correctamente",
        "lat": 9.934739, 
        "lon": -84.087502,
        "usuario": "Sensor de semáforo"
    },
    {
        "tipo": "Ruido excesivo",
        "descripcion": "Nivel de ruido supera el límite permitido",
        "lat": 9.927129,
        "lon": -84.082012,
        "usuario": "Sensor de ruido"
    },
    {
        "tipo": "Fuga de agua",
        "descripcion": "Se detecta una fuga de agua en la zona",
        "lat": 9.912345,
        "lon": -84.071789,
        "usuario": "Sensor de agua"
    }
]

# Función para enviar un mensaje al broker MQTT
def send_report(client, report):
    try:
        message = json.dumps(report)
        client.publish(TOPIC, message)
        print(f"Reporte enviado: {message}")
    except Exception as e:
        print(f"Error al enviar el reporte: {e}")

# Configuración del cliente MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT")
    else:
        print(f"Error de conexión: {rc}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "PythonPublisher")
client.on_connect = on_connect

try:
    client.connect(BROKER, PORT, 60)
    client.loop_start()

    # Enviar los reportes con un intervalo de tiempo
    for report in reports:
        send_report(client, report)
        time.sleep(1)  # Espera 1 segundo entre cada envío

    client.loop_stop()
    client.disconnect()

except Exception as e:
    print(f"Error al conectar al broker MQTT: {e}")
