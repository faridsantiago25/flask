from config.db import app, db, ma
from models.roles import Roles
from sqlalchemy import text
from marshmallow import ValidationError, fields
from validations.valitadions import validate_int,validate_str


class Empleados(db.Model):
    _tablename_ = 'empleados'
    
    id_empleados = db.Column(db.Integer, primary_key=True)
    id_rol = db.Column(db.Integer)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    activo = db.Column(db.Boolean)


    def __init__(self,id_empleados, id_rol, nombre, apellido):
        self.id_empleados = id_empleados
        self.id_rol = id_rol
        self.nombre = nombre
        self.apellido = apellido
        self.activo = True


with app.app_context():
    db.create_all()

#creamos las validaciones de los empleados
def validar_rol_id(val):
    rol_existente = db.session.query(Roles).filter_by(id_rol=val).first()

    if rol_existente is None:
        raise ValidationError("El rol no existe")

#validamos que el empleado exista comprobando si su id existe en la tabla empleados
def validar_empleado_id(val):
    raw_query = text("SELECT EXISTS(SELECT 1 FROM empleados WHERE id_empleados = :id)")
    params = {"id":val}

    emmpleado_existente = db.session.execute(raw_query,params)
    row = emmpleado_existente.fetchone()

    if row [0]==1:
        raise ValidationError("El empleado ya existe")
    
#validamos si el empleado no existe comprobando si su id  existe en la tabla empleados
def validar_no_existe(val):
    raw_query = text("SELECT EXISTS(SELECT 1 FROM empleados WHERE id_empleados = :id)")
    params = {"id":val}

    emmpleado_existente = db.session.execute(raw_query,params)
    row = emmpleado_existente.fetchone()

    if row [0]==0:
        raise ValidationError("El empleado no existe")


class EmpleadosSchema(ma.Schema):
    id_empleados = fields.Integer(required=True, allow_none=False, validate=[validate_int, validar_empleado_id])
    id_rol = fields.Integer(required=True, allow_none=False, validate=[validate_int, validar_rol_id])
    nombre = fields.Str(required=True, allow_none=False, validate=validate_str)
    apellido = fields.Str(required=True, allow_none=False, validate=validate_str)
    activo = fields.Boolean(required=True, allow_none=False)

    class Meta:
        fields = ('id_empleados', 'id_rol', 'nombre', 'apellido','activo')
       
