from flask import Blueprint,request,jsonify,session
from config.db import db
from models.roles import Roles, RolesSchema

ruta_roles = Blueprint("routes_roles", __name__) 

rol_schema = RolesSchema()
rol_schemas = RolesSchema(many=True)

# get
@ruta_roles.route('/roles', methods=['GET'])

def roles():
    resultall= Roles.query.all()
    resultRoles = rol_schemas.dump(resultall)
    return jsonify(resultRoles)


# get by id
@ruta_roles.route('/roles/<int:id>', methods=['GET'])
def rol_by_id(id):
    result = Roles.query.get(id)
    return rol_schema.jsonify(result)

# post
@ruta_roles.route('/roles', methods=['POST'])

def crear_roles():
    json_data = request.json
    errors = rol_schema.validate(json_data)

    if errors:
        return {"error":errors},422
    
    result = Roles(json_data['nombre'])
    db.session.add(result)
    db.session.commit()
    return rol_schema.jsonify(result)

# put
@ruta_roles.route('/roles/<int:id>', methods=['PUT'])
def actualizar_rol(id):
    json_data = request.json
    errors = rol_schema.validate(json_data)

    if errors:
        return {"error":errors},422
    
    result = Roles.query.get(id)
    result.nombre = json_data['nombre']
    db.session.commit()
    return rol_schema.jsonify(result)
 
# delete
@ruta_roles.route('/roles/<int:id>', methods=['DELETE'])
def eliminar_rol(id):
    rol = Roles.query.get(id)
    db.session.delete(rol)
    db.session.commit()
    return rol_schema.jsonify(rol)