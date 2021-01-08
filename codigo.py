#Importamos todas las librerias necesarias
import time
import dht_config
import RPi.GPIO as GPIO
import paho.mqtt.publish as publish
import json
import threading
from gpiozero import Servo
import smbus
import sys

#Creamos una clase para el sensor de temperatura
class SensorTemperatura:
    def __init__(self, objControl):
        self.objControl = objControl

    #Creamos una funcion que se va a encargar de tomar los valores del sensor
    def lectura(self):
        GPIO.setmode(GPIO.BCM)

        gpio_pin_sensor = 18  
 
        #Crear una instancia del sensor de temperatura. Mirad el fichero dht_config.py para detalles de configuración
        sensor = dht_config.DHT(gpio_pin_sensor) 

        while True:
            humi, temp = sensor.read()
            
            print('Humedad {0:.1f}%, Temperatura {1:.1f}'.format( humi, temp))
            self.objControl.setTemperatura(temp)
            self.objControl.setHumedad(humi)
            try:
                topic = "deustoLab/Temperatura"
                mensaje= {
                    "temp": temp,
                    "humi": humi
                }
        
                hostname = "169.254.228.91"
                mensaje_json= json.dumps(mensaje)
                publish.single("deustoLab/Temperatura", mensaje_json, hostname=hostname)
            
            except:
                pass         
                time.sleep(2)
            

    
#Creamos una clase para el sensor de gas
class SensorGas:
    
    def __init__(self, objControl):
        self.objControl = objControl
	    

    def adc_read(self):
        while True:
            bus = smbus.SMBus(1)
            address = 0x50

            REG_ADDR_RESULT = 0x00
            REG_ADDR_ALERT  = 0x01
            REG_ADDR_CONFIG = 0x02
            REG_ADDR_LIMITL = 0x03
            REG_ADDR_LIMITH = 0x04
            REG_ADDR_HYST   = 0x05
            REG_ADDR_CONVL  = 0x06
            REG_ADDR_CONVH  = 0x07
            bus.write_byte_data(address, REG_ADDR_CONFIG,0x20)

            data=bus.read_i2c_block_data(address, REG_ADDR_RESULT, 2)
            raw_val=(data[0]&0x0f)<<8 | data[1]
            print(raw_val)
            self.objControl.setGas(raw_val)
            time.sleep(1)
   
    
#Creamos una clase de control que se encargará de vigilar los valores medidos del sensor y mandar actuar en consecuencia
class Control:
    def __init__(self, objServo, objHumidificador, objVentilador):
        
        self.objServo = objServo
        self.objHumidificador = objHumidificador
        self.objVentilador = objVentilador
        self.temp = 100
        self.humi = 100
        self.gas = 100
    
    def setTemperatura(self, temp):
        self.temp = temp

    def setHumedad(self, humi):
        self.humi = humi

    def setGas(self, gas):
        self.gas = gas

    def controlar(self):
        while True:
            if self.temp <= 23:
                self.objServo.arrancarCaldera()
                #print('Ha arrancado el servo')

            if self.humi <= 50:
                self.objHumidificador.encenderHumi()

            else:
                self.objHumidificador.apagarHumi()
                '''valor_servo= "Encencida"
                topic = "deustoLab/Temperatura"
                mensaje= {
                    "valor_servo": valor_servo,
          
                }
       
                hostname = "169.254.228.91"
                mensaje_json= json.dumps(mensaje)
                publish.single("deustoLab/Temperatura", mensaje_json, hostname=hostname)''' 
                
            #if self.gas >= 270:
                #self.objVentilador.arrancarVentilador()
                #print('Ha arrancado el ventila')
            #else:
                #self.objVentilador.pararVentilador()
                #print('ventilador parado')'''

           
            time.sleep(1)

#Creamos una clase que crea y arranca el ventilador
class Ventilador:
    
    GPIO.setwarnings(False)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)

    def pararVentilador(self):
        try:
           

            GPIO.output(17, GPIO.LOW)
            time.sleep(1)


        except KeyboardInterrupt:
            # here you put any code you want to run before the program
            # exits when you press CTRL+C
            print ("keyboard Interrupt")

        except:

            print ("other error")

    def arrancarVentilador(self):

        try:
          

            GPIO.output(17, GPIO.HIGH)
            time.sleep(1)
                


        except KeyboardInterrupt:
            # here you put any code you want to run before the program
            # exits when you press CTRL+C
            print ("keyboard Interrupt")

        except:

            print ("other error")


#Creamos una clase que crea y arranca el servo
class Servomotor:
    def arrancarCaldera(self):

        myGPIO=17


        myCorrection=0.45
        maxPW=(2.0+myCorrection)/1000
        minPW=(1.0-myCorrection)/1000

        myServo = Servo(myGPIO,min_pulse_width=minPW,max_pulse_width=maxPW)

        print("Using GPIO17")
        print("Max pulse width is set to 2.45 ms")
        print("Min pulse width is set to 0.55 ms")
  
        for value in range(0,21):
            value2=(float(value)-10)/10
            myServo.value=value2
            time.sleep(1)

#Creamos una clase para el humidificador
class Humidificador:
    def encenderHumi(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
    
        GPIO.setup(14, GPIO.OUT) # GPIO 14 como ouput
        GPIO.output(14, GPIO.HIGH) #  atomize
        

    def apagarHumi(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
    
        GPIO.setup(14, GPIO.OUT) # GPIO 14 como ouput
        GPIO.output(14, GPIO.LOW) #  STOP atomize



def main():
    objServo = Servomotor()
    objVentilador = Ventilador()
    objHumidificador = Humidificador()
    objControl = Control(objServo, objHumidificador, objVentilador)
    objSensorTemperatura = SensorTemperatura(objControl)
    objSensorGas = SensorGas(objControl)

    hilo1 = threading.Thread(target=objSensorTemperatura.lectura,)
    #hilo2 = threading.Thread(target=objSensorGas.adc_read,)
    hilo3 = threading.Thread(target=objControl.controlar,)
    hilo1.start()
    #hilo2.start()
    hilo3.start()
    print ("fin del main")
 
if __name__ == '__main__':
    main()
