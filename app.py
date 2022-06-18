from flask import Flask
from flask_pymongo import PyMongo

#Inicializo en mi variable app una instancia de Flask
app = Flask(__name__)

#configuro la url donde se creara la base de datos
app.config['MONGO_URI'] = 'mongodb://localhost/tiendadb'

#instancio en una variable la base de datos de mongo pasandole como parametro mi aplicación
mongo = PyMongo(app)

#importo la instancia de Blueprint almacenada en 'usuarios' del archivo rutas_usuarios
# y lo registro en mi aplicación como un blueprint
from rutas_usuarios import usuarios
app.register_blueprint(usuarios)

#runeo la aplicación
if __name__ == '__main__':
    app.run(debug=True)