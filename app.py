from flask import Flask,render_template

temperatura=22
humedad=27


# Inicializamos la aplicacion
app = Flask(__name__)
 
# Ruta principal 

@app.route("/")
def index():
    templateData = {'sensorTemp' : temperatura,'sensorHum' : humedad}  
    return render_template('index.html',**templateData)
    
# Configuracion basica
if __name__ == '__main__':
    # Activamos debug y configuramos para que sea accesible desde cualquier dispositivo
    app.run(debug=True, host='0.0.0.0')
