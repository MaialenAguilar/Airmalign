# -----------------------------------
#     MQTT CLIENT DEMO 
# -----------------------------------

 
import paho.mqtt.client as mqtt
import json
from flask import Flask
from datetime import datetime

topic = "deustoLab/Temperatura"


# Callback que se llama cuando el cliente recibe el CONNACK del servidor 
#Restult code 0 significa conexion sin errores
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Nos subscribirmos al topic 
    client.subscribe(topic)
 #-----------------------------------------------
# Callback que se llama "automaticamente" cuando se recibe un mensaje del Publiser.
def on_message(client, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")
    mensaje_recibido = msg.payload
    print(msg.topic+" "+mensaje_recibido)

    #the message received starts with 'b, that mean bytes. 
    mensaje_recibido_json =json.loads(msg.payload )
   
    temp=mensaje_recibido_json["temp"]
    print(temp)

    hum=mensaje_recibido_json["humi"]
    print(hum)

    f=open("DatosFlask.py","w")
    f.write("Temperatura=" + str(temp) + "\nHumedad=" + str(hum))
    time.sleep(10)
    f.close()



 #-----------------------------------------------
 # Creamos un cliente MQTT 
client = mqtt.Client()

#Definimos los callbacks para conectarnos y subscribirnos al topic
client.on_connect = on_connect
client.on_message = on_message

#Para la actividad 1: usad la IP de la RPi que actua como broker
hostname ="169.254.228.91"

 
client.connect(hostname , 1883, 60)
client.loop_forever()