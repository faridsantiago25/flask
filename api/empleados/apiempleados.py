from flask import Blueprint, request, jsonify
from config.db import db
from models.empleados import Empleados, EmpleadosSchema
from sqlalchemy import text
from marshmallow import ValidationError
import json

ruta_empleados = Blueprint("routes_empleados", __name__)
empleado_schema = EmpleadosSchema()
empleado_schemas = EmpleadosSchema(many=True)

# get
@ruta_empleados.route('/empleados', methods=['GET'])

def lista_empleados():
    result = db.session.execute(text(""" SELECT empleados.id_empleados, empleados.nombre, empleados.apellido, roles.nombre ,
                                     roles.id_rol, empleados.activo FROM empleados JOIN roles ON roles.id_rol = empleados.id_rol """))
    
    resultall = result.fetchall()

    total_empleados = []

    for empleados in resultall:
        json = {
            "id_empleados": empleados[0],
            "nombre": empleados[1],
            "apellido": empleados[2],
            "rol": empleados[3],
            "id_rol": empleados[4],
            "activo": empleados[5]
        }
        total_empleados.append(json)

    return jsonify(total_empleados)

#post
@ruta_empleados.route('/empleados', methods=['POST'])
def create_empleado():
    json_data = request.json
    errors = empleado_schema.validate(json_data)

    if errors:
        return {"error":errors},422
    
    result = Empleados(json_data['id_empleados'],json_data['id_rol'],json_data['nombre'],json_data['apellido'])
    db.session.add(result)
    db.session.commit()
    return empleado_schema.jsonify(result)


#get by id
@ruta_empleados.route('/empleados/<int:id>', methods=['GET'])
def empleado_by_id(id):

    result = db.session.execute(text(""" SELECT empleados.id_empleados, empleados.nombre, empleados.apellido, roles.nombre,
                                     roles.id_rol, empleados.activo FROM empleados JOIN roles ON roles.id_rol = empleados.id_empleados WHERE empleados.id_empleados = :id"""),{"id":id})
    result = result.fetchone()

    json = {
        "id_empleados": result[0],
        "nombre": result[1],
        "apellido": result[2],
        "rol": result[3],
        "id_rol": result[4],
        "activo": result[5]
    }
    return jsonify(json)

#put
@ruta_empleados.route('/empleados/<int:id>', methods=['PUT'])

def update_empleado(id):
    json_data = request.json

    result = Empleados.query.get(id)
    result.id = json_data["id_empleados"]
    result.nombre = json_data["nombre"]
    result.apellido = json_data["apellido"]
    result.id_rol = json_data["id_rol"]
    result.activo = json_data["activo"]

    db.session.commit()
    return empleado_schema.jsonify(result)

#delete
@ruta_empleados.route('/empleados/<int:id>', methods=['DELETE'])
def delete_empleado(id):
    result = Empleados.query.get(id)
    result.activo = False
    db.session.commit()
    return empleado_schema.jsonify(result)
    
