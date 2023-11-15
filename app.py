from api.rol.apirol import ruta_roles
from api.empleados.apiempleados import ruta_empleados
from api.productos.apiproductos import ruta_productos
from api.produccion.apiproduccion import ruta_produccion
from api.authenticator import authenticator_routes
from flask import Flask, request, jsonify, redirect, render_template
from config.db import app
from dotenv import load_dotenv
from flask_cors import CORS
from internal.authentication import validate_token

#app.register_blueprint(authenticator_routes)

#@ruta_empleados.before_request
#@ruta_productos.before_request
#@ruta_produccion.before_request
#@ruta_roles.before_request

#def if_logged_into():
#    request_parameters = request.args

#    if request_parameters.get('Authorization') == None:
#        response = jsonify({"message": "Token not found"})
#        response.status_code = 404
#        return response
    
#    token = request_parameters.get('Authorization').split(" ")[1]
#    return validate_token(token, False)

app.register_blueprint(ruta_empleados)
app.register_blueprint(ruta_productos)
app.register_blueprint(ruta_produccion)
app.register_blueprint(ruta_roles)

CORS(app,resources={r"/*": {"origins": "*"}})


if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True, port=5000, host="0.0.0.0")
