from flask import Blueprint,redirect,request,jsonify
from config.db import app, db, ma
from models.productos import Productos, ProductosSchema

ruta_productos = Blueprint("routes_productos", __name__)

producto_schema = ProductosSchema()
producto_schemas = ProductosSchema(many=True)

#get
@ruta_productos.route('/productos', methods=['GET'])
def list_productos():
    resultall= Productos.query.all()
    resultProductos = producto_schemas.dump(resultall)
    return jsonify(resultProductos)

#get by id

@ruta_productos.route('/productos/<int:id>', methods=['GET'])
def get_productos(id):
    producto = Productos.query.get(id)
    return producto_schema.jsonify(producto)


#post
@ruta_productos.route('/productos', methods=['POST'])
def agregar_producto():
    errs = producto_schema.validate(request.json)
    if errs:
         return {"error": errs}, 422

    id_productos = request.json['id_productos']
    nombre = request.json['nombre']
    precio = request.json['precio']
    compensacion_unidad = request.json['compensacion_unidad']
    compensacion_paquete = request.json['compensacion_paquete']
    tipo = request.json['tipo']

    nuevo_producto = Productos(id_productos,nombre,precio,compensacion_unidad,compensacion_paquete,tipo)
    db.session.add(nuevo_producto)
    db.session.commit()
    return producto_schema.jsonify(nuevo_producto)


#put
@ruta_productos.route('/productos/<int:id>', methods=['PUT'])
def update_productos(id):
    errs = producto_schema.validate(request.json)
    if errs:
         return {"error": errs}, 422

    producto = Productos.query.get(id)
    id_productos = request.json['id_productos']
    nombre = request.json['nombre']
    precio = request.json['precio']
    compensacion_unidad = request.json['compensacion_unidad']
    compensacion_paquete = request.json['compensacion_paquete']
    tipo = request.json['tipo']

    producto.id_productos = id_productos
    producto.nombre = nombre
    producto.precio = precio
    producto.compensacion_unidad = compensacion_unidad
    producto.compensacion_paquete = compensacion_paquete
    producto.tipo = tipo

    db.session.commit()
    return producto_schema.jsonify(producto)

#delete
@ruta_productos.route('/productos/<int:id>', methods=['DELETE'])
def delete_productos(id):
    producto = Productos.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return producto_schema.jsonify(producto)