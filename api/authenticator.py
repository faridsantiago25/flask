from flask import Blueprint, request, jsonify
from internal.authentication import new_token,validate_token
from config.db import db
from sqlalchemy import text

authenticator_routes = Blueprint("authenticator_routes", __name__)

@authenticator_routes.route('/login', methods=['POST'])

def login():
    data = request.get_json()
    id = data['id_empleados']

    if id == "":
        response = jsonify({"message": "Credentials are required"})
        response.status_code = 400
        return response
    
    result = db.session.execute(text("SELECT empleados.id_empleados, empleados.nombre, empleados.apellido, roles.nombre FROM empleados JOIN roles ON roles.id_rol=empleados.id_rol WHERE empleados.id_empleados = :id"),{"id":id})
    result = result.fetchone()

    if result == None:
        response = jsonify({"message": "User not found :( "})
        response.status_code = 404
        return response
    
    payload = {
        "id_empleados": result[0],
        "nombre": result[1],
        "apellido": result[2],
        "id_rol": result[3]
    }
    return jsonify(new_token(payload).decode('UTF-8'))

@authenticator_routes.route("/verify/token")
def verify():
    token = request.headers['authorization'].split(" ")[1]
    return validate_token(token, True)
