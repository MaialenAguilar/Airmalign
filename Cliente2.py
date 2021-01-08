# -----------------------------------
#     MQTT CLIENT DEMO 
# -----------------------------------

 
import paho.mqtt.client as mqtt
import json
from flask import Flask
from datetime import datetime
import time
import os

topic = "deustoLab/gas"

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
     
    gas=mensaje_recibido_json["gas"]
    print(gas)
  
	
    f=open("app.py","a")
    f.write("\ngas=" + str(gas) + "\napp = Flask(__name__)" +"\n@app.route(" + "'/'" + ")"+ "\ndef index():" + "\n    templateData = {" +"'sensorTemp'" + " : temperatura,"+ "'sensorHum'" + " : humedad," +"'sensorGas'" + " : gas }" + "\n    return render_template("+ "'index.html'"+ ",**templateData)" + "\nif __name__ ==" +  "'__main__'"+ ":" + "\n      app.run(debug=True, host=" +"'0.0.0.0'"+ ")")
    time.sleep(2)
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

os.system("flask run")