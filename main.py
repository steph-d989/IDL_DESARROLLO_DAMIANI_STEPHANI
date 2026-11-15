### IMPORTACION DE LIBRERIAS
from flask import Flask, jsonify, request, render_template

### CREAR INSTANCIA DE FLASK
app = Flask(__name__)

### CREAR RUTAS DEL PROYECTO
@app.route("/") #PAGINA PRINCIPAL
def home():
    return render_template('index.html')

@app.route("/products") #PAGINA PRODUCTOS
def productos():
    return render_template('productos.html')

@app.route("/models") #PAGINA MODELOS
def modelo():
    return render_template('modelo.html')

if __name__ == '__main__':
    app.run(debug=True)