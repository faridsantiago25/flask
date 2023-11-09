from flask import Blueprint,request,jsonify
from config.db import db
from models.produccion import Produccion, ProduccionSchema
from models.produccion_empleados import ProduccionEmpleado, ProduccionEmpleadoSchema
from sqlalchemy import text

ruta_produccion = Blueprint("routes_produccion", __name__)

produccion_schema = ProduccionSchema()
produccion_schemas = ProduccionSchema(many=True)

#get
@ruta_produccion.route('/produccion/<int:id>', methods=['GET'])
@ruta_produccion.route('/produccion', methods=['GET'])
def produccion(id_empleado = None):

    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    #print(fecha_inicio)

    if id_empleado == None:
        result = ProduccionEmpleado.Total(fecha_inicio,fecha_fin)
        return jsonify(result)
    
    result = ProduccionEmpleado.produccion_por_empleado(id_empleado,fecha_inicio,fecha_fin)
    return jsonify(result)

#get produccion total by ID
@ruta_produccion.route('/produccion/total/<int:id>', methods=['GET'])
def produccion_por_empleado(id):
    result = db.session.execute(text("""SELECT produccion.id_produccion,empleados.nombre, empleados.apellido, roles.nombre AS rol, cantidad, 
                                     produccion.fecha, produccion.id_producto, produccion.id_empleado, productos.nombre AS nombre_producto 
                                     FROM produccion JOIN productos ON productos.id_productos = produccion.id_producto
                                     JOIN empleados ON empleados.id_empleados = produccion.id_empleado
                                     JOIN roles ON roles.id_rol = empleados.id_rol WHERE produccion.id_empleado = :id"""),{"id":id})
    
    result = result.fetchone()

    json = {
        "id_produccion": result[0],
        "nombre": result[1],
        "apellido": result[2],
        "rol": result[3],
        "cantidad": result[4],
        "fecha": result[5],
        "id_producto": result[6],
        "id_empleado": result[7],
        "nombre_producto": result[8]
    }
    return jsonify(json)

#get produccion total
@ruta_produccion.route('/produccion/total', methods=['GET'])
def produccion_total():
    result = db.session.execute(text(""" SELECT produccion.id_produccion,empleados.nombre, empleados.apellido, roles.nombre AS rol, cantidad,
                                     produccion.fecha, produccion.id_producto, produccion.id_empleado, productos.nombre AS nombre_producto
                                     from produccion JOIN productos ON productos.id_productos = produccion.id_producto 
                                     JOIN empleados ON empleados.id_empleados = produccion.id_empleado
                                     JOIN roles ON roles .id_rol = empleados.id_rol""")) 
    
    result = result.fetchall() 

    json = []

    for produccion in result:
        new={
            "id_produccion": produccion[0],
            "nombre_empleado": produccion[1],
            "apellido_empleado": produccion[2],
            "rol_empleado": produccion[3],
            "cantidad": produccion[4],
            "fecha": produccion[5],
            "id_producto": produccion[6],
            "id_empleado": produccion[7],
            "nombre_producto": produccion[8]
        }
        json.append(new)
        
    return jsonify(json)


#post
#formato de la fecha 2021-05-05 00:00:00 (sino muestra mensaje de que no es valida la fecha)
@ruta_produccion.route('/produccion', methods=['POST'])
def agregar_produccion():
    id_produccion = request.json['id_produccion']
    id_empleado = request.json['id_empleado']
    id_producto = request.json['id_producto']
    cantidad = request.json['cantidad']
    fecha = request.json['fecha']

    nueva_produccion = Produccion(id_produccion,id_empleado,id_producto,cantidad,fecha)
    db.session.add(nueva_produccion)
    db.session.commit()
    return produccion_schema.jsonify(nueva_produccion)

#put
@ruta_produccion.route('/produccion/<int:id>', methods=['PUT'])
def update_produccion(id):

    errs = produccion_schema.validate(request.json)
    if errs:
         return {"error": errs}, 422
    
    produccion = Produccion.query.get(id)
    id_produccion = request.json['id_produccion']
    id_empleado = request.json['id_empleado']
    id_producto = request.json['id_producto']
    cantidad = request.json['cantidad']
    fecha = request.json['fecha']

    produccion.id_produccion = id_produccion
    produccion.id_empleado = id_empleado
    produccion.id_producto = id_producto
    produccion.cantidad = cantidad
    produccion.fecha = fecha

    db.session.commit()
    return produccion_schema.jsonify(produccion)

#delete
@ruta_produccion.route('/produccion/<int:id>', methods=['DELETE'])
def delete_produccion(id_produccion):
    produccion = Produccion.query.get(id_produccion)
    db.session.delete(produccion)
    db.session.commit()
    return produccion_schema.jsonify(produccion)
