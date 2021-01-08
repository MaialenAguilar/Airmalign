temperatura=23
humedad=51
from flask import Flask,render_template
gas=216
app = Flask(__name__)
@app.route('/')
def index():
    templateData = {'sensorTemp' : temperatura,'sensorHum' : humedad,'sensorGas' : gas }
    return render_template('index.html',**templateData)
if __name__ =='__main__':
      app.run(debug=True, host='0.0.0.0')
gas=215
app = Flask(__name__)
@app.route('/')
def index():
    templateData = {'sensorTemp' : temperatura,'sensorHum' : humedad,'sensorGas' : gas }
    return render_template('index.html',**templateData)
if __name__ =='__main__':
      app.run(debug=True, host='0.0.0.0')
gas=215
app = Flask(__name__)
@app.route('/')
def index():
    templateData = {'sensorTemp' : temperatura,'sensorHum' : humedad,'sensorGas' : gas }
    return render_template('index.html',**templateData)
if __name__ =='__main__':
      app.run(debug=True, host='0.0.0.0')
gas=216
app = Flask(__name__)
@app.route('/')
def index():
    templateData = {'sensorTemp' : temperatura,'sensorHum' : humedad,'sensorGas' : gas }
    return render_template('index.html',**templateData)
if __name__ =='__main__':
      app.run(debug=True, host='0.0.0.0')