from pathlib import Path
import csv

from flask import Flask, render_template, request
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier

BASE = Path(__file__).resolve().parent
app = Flask(__name__)

CATEGORIAS = {
    'Suplementos nutricionales': 'Productos de apoyo nutricional.',
    'Higiene y bioseguridad': 'Productos destinados a la limpieza y la bioseguridad de instalaciones.',
    'Insumos de manejo': 'Productos de apoyo para el manejo general de los animales.',
}



def entrenar_modelo():

    with (BASE / 'data' / 'entrenamiento.csv').open(
        encoding='utf-8-sig',
        newline=''
    ) as f:

        lector = csv.DictReader(
            linea for linea in f if linea.strip()
        )

        ejemplos = list(lector)

    entradas = [
        [
            fila['especie'],
            fila['etapa'],
            fila['necesidad']
        ]
        for fila in ejemplos
    ]

    salidas = [
        fila['categoria']
        for fila in ejemplos
    ]

    modelo = Pipeline([
        ('codificacion', ColumnTransformer([
            ('categorias', OneHotEncoder(handle_unknown='ignore'), [0, 1, 2])])),
        ('arbol', DecisionTreeClassifier(
            max_depth=3,
            random_state=42
        ))
    ])

    modelo.fit(entradas, salidas)

    print("Modelo de IA entrenado correctamente")
    print("Registros utilizados:", len(ejemplos))

    return modelo, len(ejemplos)

MODELO, NUM_EJEMPLOS = entrenar_modelo()


@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/products')
def productos():
    return render_template('productos.html')


@app.route('/models', methods=['GET', 'POST'])
def modelos():
    resultado = None
    valores = {
        'especie': 'Cerdo',
        'etapa': 'Joven',
        'necesidad': 'Nutrición'
    }
    error = None

    if request.method == 'POST':
        valores = {
            campo: request.form.get(campo, '')
            for campo in valores
        }

        validos = {
            'especie': {'Cerdo', 'Pollo', 'Bovino'},
            'etapa': {'Joven', 'Adulto'},
            'necesidad': {'Nutrición', 'Higiene', 'Manejo'},
        }

        if not all(
            valores[k] in opciones
            for k, opciones in validos.items()
        ):
            error = 'Selecciona opciones válidas en todos los campos.'
        else:
            categoria = MODELO.predict([[
                valores['especie'],
                valores['etapa'],
                valores['necesidad']
            ]])[0]

            resultado = {
                'categoria': categoria,
                'descripcion': CATEGORIAS[categoria]
            }

    return render_template(
        'modelo.html',
        resultado=resultado,
        error=error,
        valores=valores,
        num_ejemplos=NUM_EJEMPLOS
    )


if __name__ == '__main__':
    app.run(debug=True)
