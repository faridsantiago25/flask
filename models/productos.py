from config.db import app, db, ma
from sqlalchemy import text
from marshmallow import fields, ValidationError
from validations.valitadions import validate_str, validate_int, validate_float

class Productos(db.Model):
    _tablename_ = 'productos'
    id_productos = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45))
    precio = db.Column(db.Float)
    compensacion_unidad = db.Column(db.Float, nullable=True)
    compensacion_paquete = db.Column(db.Float, nullable=True)
    tipo = db.Column(db.String(45))

    def __init__(self,id_productos, nombre, precio, compensacion_unidad, compensacion_paquete, tipo):
        self.id_productos = id_productos
        self.nombre = nombre
        self.precio = precio
        self.compensacion_unidad = compensacion_unidad
        self.compensacion_paquete = compensacion_paquete
        self.tipo = tipo
        
with app.app_context():
    db.create_all()

def validar_producto(val):
    #verificamos si el nombre del producto existe en la tabla productos
    val = val.lower()
    raw_query = text("SELECT EXISTS(SELECT 1 FROM productos WHERE LOWER(nombre) = :nombre)")
    params = {'nombre':val}

    producto_existente = db.session.execute(raw_query,params)
    row = producto_existente.fetchone()

    if row[0] == 1:
        raise ValidationError("El producto ya existe")

def validar_id_producto(val):
    #verificamos si el id del producto existe en la tabla productos

    raw_query = text("SELECT EXISTS(SELECT 1 FROM productos WHERE id_productos = :id)")
    params = {'id':val}

    producto_existente = db.session.execute(raw_query,params)
    row = producto_existente.fetchone()

    if row[0] == 0:
        raise ValidationError("El id del producto no existe")

def validar_tipo_producto(val):
    #verificamos si el tipo del producto es valido
    val = val.lower()
    if val != "guarnecedor" and val != "cortador" and val != "ensamblador":
        raise ValidationError("El tipo de producto no es valido")


class ProductosSchema(ma.Schema):
    id_productos = fields.Integer(allow_none=False)
    nombre = fields.String(allow_none=False, validate=[validate_str, validar_producto])
    precio = fields.Float(required=True, allow_none = False, validate=[validate_float])
    compensacion_unidad = fields.Float(required=True, allow_none = False, validate=[validate_float])
    compensacion_paquete = fields.Float(required=True, allow_none = False, validate=[validate_float])
    tipo = fields.String(required=True, allow_none = False, validate=[validate_str, validar_tipo_producto])

    class Meta:
        fields = ('id_productos', 'nombre', 'precio', 'compensacion_unidad', 'compensacion_paquete','tipo')


