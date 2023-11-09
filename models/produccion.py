from config.db import app, db, ma
from models.roles import Roles
from marshmallow import ValidationError, fields, validates_schema
from sqlalchemy import text
from validations.valitadions import validate_int,validate_str,validate_float
from models.empleados import validar_no_existe
from models.productos import validar_id_producto

class Produccion(db.Model):
    _tablename_ = 'produccion'

    id_produccion = db.Column(db.Integer, primary_key=True)
    id_empleado = db.Column(db.Integer)
    id_producto = db.Column(db.Integer)
    cantidad = db.Column(db.Integer)
    fecha = db.Column(db.DateTime)

    def __init__(self,id_produccion, id_empleado, id_producto, cantidad, fecha):
        self.id_produccion = id_produccion
        self.id_empleado = id_empleado
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.fecha = fecha

    #esta query se utiliza para obtener la produccion de un empleado en un rango de fechas
    def Produccion_empleados(id_empleado):
        results = db.session.execute(text(""" SELECT SUM(produccion.cantidad) AS cantidad_total, empleados.nombre, empleados.apellido, produccion.fecha,
                                          productos.nombre, productos.compensacion_unidad, productos.compensacion_paquete FROM produccion
                                          JOIN productos ON productos.id_productos = produccion.id_producto
                                          JOIN empleados ON empleados.id_empleados = produccion.id_empleado
                                          WHERE empleados.id_empleados = :id_empleado GROUP BY empleados.nombre, empleados.apellido, produccion.fecha,
                                          productos.nombre, productos.id_productos"""),)
        
        return results
    


with app.app_context():
    db.create_all()

class ProduccionSchema(ma.Schema):

    id_produccion = fields.Integer(allow_none=False)
    id_empleado = fields.Integer(allow_none=False, validate=[validate_int, validar_no_existe])
    id_producto = fields.Integer(allow_none=False, validate=[validate_int,validar_id_producto])
    cantidad = fields.Integer(allow_none=False, validate=[validate_int])
    fecha = fields.DateTime(allow_none=False,requeired=True)

    @validates_schema(skip_on_field_errors=False)
    def validar_producto_usuario(self, data, **kwargs):
        id_producto = data.get('id_producto')
        id_empleado = data.get('id_empleado')

        #creamos un query para obtener el producto de la tabla productos y verificamos que el producto es valido
        
        rawquery = text("SELECT LOWER(tipo) FROM productos WHERE id_productos = :id")
        params = {'id':id_producto}
        producto_existente = db.session.execute(rawquery,params)
        result1 = producto_existente.fetchone()

        #creamos un query para obtener el empleado de la tabla empleados y verificamos que el empleado es valido
        rawquery = text("SELECT LOWER(roles.nombre) FROM empleados JOIN roles ON roles.id_rol = empleados.id_rol WHERE id_empleados = :id")
        params = {'id':id_empleado}
        empleado_existente = db.session.execute(rawquery,params)
        result2 = empleado_existente.fetchone()

        if result1[0] != result2[0]:
            raise ValidationError('El empleado no puede producir este producto')

    class Meta:
        fields = ('id_produccion', 'id_empleado', 'id_producto', 'cantidad', 'fecha')



        

