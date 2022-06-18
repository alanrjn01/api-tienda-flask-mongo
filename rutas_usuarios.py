from bson import ObjectId
from bson import json_util
from flask import jsonify,request,Blueprint,Response,make_response
from kiwisolver import BadRequiredStrength
from werkzeug.security import generate_password_hash, check_password_hash
#creo una instancia de blueprint en usuarios
usuarios = Blueprint('usuarios',__name__)
#importo la variable 'mongo' de mi archivo app.py para poder acceder a la base de datos
from app import mongo

#obtengo los datos del request, compruebo si no están vacíos y realizo una inserción
#en la base de datos, posteriormente devuelvo el usuario creado
#con try y except compruebo si los campos para crear el usuario son los necesarios, de no ser asi
#lanzo un bad request, y si alguno de los campos estan vacios, se devuelve un bad request igualmente
#si se crea el usuario devuelvo un json con los datos del usuario creado
@usuarios.route('/usuario', methods=['POST'])
def crear_usuario():
    try:
        nombre = request.json['nombre']
        contrasenia = request.json['contrasenia']
        celular = request.json['celular']
        direccion = request.json['direccion']  
        if nombre and contrasenia and celular and direccion:
            contrasenia_cifrada = generate_password_hash(contrasenia)
            usuario = mongo.db.usuario.insert_one(
                {
                    'nombre' : nombre,
                    'contrasenia' : contrasenia_cifrada,
                    'celular' : celular,
                    'direccion' : direccion
                })
            respuesta = {
                    '_id' : usuario.inserted_id,
                    'nombre' : nombre,
                    'contrasenia' : contrasenia_cifrada,
                    'celular' : celular,
                    'direccion' : direccion
            }
            return Response(json_util.dumps(respuesta),mimetype='application/json',status=201)
        else:
            return bad_request("Los campos necesarios no están completos")
    except:
        return bad_request("Faltan campos para completar la petición")


#planteo un try y except que envuelva la funcion
#el try recoje los datos de la request y los guarda en variables.
#con la id que se recibe en la url se busca al usuario a actualizar y utiliza sus atributos
#para compararlos con los de la request, si son iguales no se realiza ningun cambio
#y se devuelve un mensaje en json que lo aclara
#si alguno de los datos es distinto se realiza el update en la base de datos y se devuelve un json
#con los datos nuevos
#el except se activa si no se recibieron los datos necesarios para actualizar
@usuarios.route('/usuario/<string:id>', methods=['PUT'])
def actualizar_usuario(id):
    try:
        nombre = request.json['nombre']
        celular = request.json['celular']
        direccion = request.json['direccion']
        datosUsuario = mongo.db.usuario.find_one({'_id':ObjectId(id)})
        if (nombre != datosUsuario['nombre']) or (celular != datosUsuario['celular']) or (direccion != datosUsuario['direccion']):
            usuarioActualizado= mongo.db.usuario.find_one_and_update({'_id':ObjectId(id)},{'$set':{
                        'nombre' : nombre,
                        'celular' : celular,
                        'direccion' : direccion
            }})
            return Response(json_util.dumps(request.json),mimetype='application/json',status=201)
        else:
            respuesta = jsonify({'Mensaje':'Los datos no han cambiado'})
            return make_response(respuesta)
    except:
        return bad_request(id)
        

#recibo una id en la url y busco y elimino en la base de datos al documento que coincida con esa id
#y devuelvo el documento eliminado en json
#si no se encuentra ninguno se devuelve un not found
@usuarios.route('/usuario/<string:id>', methods=['DELETE'])
def eliminar_usuario(id):
        usuario = mongo.db.usuario.find_one_and_delete({
            "_id":ObjectId(id)
        })
        if usuario == None:
            return not_found(usuario)
        return Response(json_util.dumps(usuario),mimetype='application/json')

#realizo una busqueda en la base de datos de la coleccion usuarios y devuelvo
#todos sus documentos en json
@usuarios.route('/usuario',methods=['GET'])
def obtener_todos_los_usuarios():
        usuario = mongo.db.usuario.find()
        return Response(json_util.dumps(usuario),mimetype='application/json', status=200)

#a partir de un id que recibo por url realizo una busqueda en la base de datos y lo devuelvo en json
#si el resultado es "None" (no se encuentra ninguno con esa id) se devuelve un not found
@usuarios.route('/usuario/<string:id>',methods=['GET'])
def obtener_usuario(id):
        usuario = mongo.db.usuario.find_one({"_id":ObjectId(id)})
        if usuario == None:
            return not_found(usuario)
        return Response(json_util.dumps(usuario),mimetype='application/json', status= 200)


#devuelve una respuesta (json) y un codigo de error 404: not found
@usuarios.errorhandler(404)
def not_found(error='error'):
    respuesta = jsonify({'error':'not found','information':error})
    return make_response(respuesta, 404)

#devuelve una respuesta (json) y un codigo de error 404: bad request
@usuarios.errorhandler(400)
def bad_request(error='error'):
    respuesta = jsonify({'error':'bad request','information':error})
    return make_response(respuesta,400)
