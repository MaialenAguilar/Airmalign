#@Laura Arjona
#@Sistemas Embebidos. 2020


# Programa ejemplo de uso del sensor digital de temperatura y humedad DHT11

import time
import dht_config
import RPi.GPIO as GPIO
import paho.mqtt.publish as publish
import json

def main():
    
     
    GPIO.setmode(GPIO.BCM)

    gpio_pin_sensor = 18   
    #Crear una instancia del sensor de temperatura. Mirad el fichero dht_config.py para detalles de configuración
    sensor = dht_config.DHT(gpio_pin_sensor) #Pasar por argumento el número del GPIO
    
    while True:
        humi, temp = sensor.read()
        print('Humedad {0:.1f}%, Temperatura {1:.1f}'.format( humi, temp))
        if temp <= 19:
           import os
           os.system('python3 ServoMotor.py')
           print('Humedad {0:.1f}%, Temperatura {1:.1f}'.format( humi, temp))

        time.sleep(1)

        

 
if __name__ == '__main__':
    main()

