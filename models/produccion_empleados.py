from config.db import db, ma, app
from sqlalchemy import text
from marshmallow import fields

class ProduccionEmpleado(db.Model):
    id_produccion_empleado = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    nombre_producto = db.Column(db.String(50))
    compensacion_unidad = db.Column(db.Float)
    compensacion_paquete = db.Column(db.Float)
    cantidad_total = db.Column(db.Integer)
    fecha = db.Column(db.DateTime)
    precio = db.Column(db.Integer)

    def _init_(self, id_produccion_empleado, nombre, apellido, nombre_producto, compensacion_unidad, compensacion_paquete, cantidad_total, fecha, precio):
        self.id_produccion_empleado = id_produccion_empleado
        self.nombre = nombre
        self.apellido = apellido
        self.nombre_producto = nombre_producto
        self.compensacion_unidad = compensacion_unidad
        self.compensacion_paquete = compensacion_paquete
        self.cantidad_total = cantidad_total
        self.fecha = fecha
        self.precio = precio

    def calculo_compensacion_paquete(produccion):
        
        new = {

        }
        #calculamos el precio del paquete y la compensacion del paquete
        precioPaquete = produccion['precio'] * 12
        compensacionPaquete = precioPaquete * (produccion['compensacion_paquete'] / 100)

        #añadims la copensacion del paquete y el precio del paquete al objeto

        new['compensacion'] = compensacionPaquete
        new['precio'] = precioPaquete
        new['nombre'] = produccion['nombre']
        new['cantidad'] = 12
        new['precio_unidad'] = produccion['precio']
        new['porcentaje'] = produccion['compensacion_paquete']
        new['nombre_empleado'] = produccion['nombre'] + ' ' + produccion['apellido']

        return new
    
    def calculo_compensacion_unidad(produccion,restante):

        new = {

        }
        
        precioRestante = restante * produccion['precio']
        new['compensacion'] = precioRestante * (produccion['compensacion_unidad'] / 100)
        new['precio'] = precioRestante
        new['nombre'] = produccion['nombre']
        new['cantidad'] = restante
        new['precio_unidad'] = produccion['precio']
        new['porcentaje'] = produccion['compensacion_unidad']
        new['nombre_empleado'] = produccion['nombre'] + ' ' + produccion['apellido']

        return new
    
    def objeto_final_build(produccion,objeto_final,objeto_produccion):
        produccion['compensacion_unidad']= float(produccion['compensacion_unidad'])
        produccion['compensacion_paquete']= float(produccion['compensacion_paquete'])
        produccion['cantidad_total']= int(produccion['cantidad_total'])
        produccion['fecha']= str(produccion['fecha'])
        produccion['precio']= int(produccion['precio'])

        if produccion['cantidad_total'] >= 12:
            new = ProduccionEmpleado.calculo_compensacion_paquete(produccion)
            objeto_final.append(new)
            restante = produccion['cantidad_total'] % 12

            if restante > 0:
                new = ProduccionEmpleado.calculo_compensacion_unidad(produccion,restante)
                objeto_final.append(new)
        
        elif produccion['cantidad_total'] == 12:
            new = ProduccionEmpleado.calculo_compensacion_paquete(produccion)
            objeto_final.append(new)
        
        else:
            new = ProduccionEmpleado.calculo_compensacion_unidad(produccion, restante)
            objeto_final.append(new)

        objeto_produccion['produccion'] = objeto_final

    def produccion_por_empleado(id_empleado,fecha_inicio, fecha_fin):
        if fecha_inicio == None:
            fecha_inicio = '1999-01-01'
        
        if fecha_fin == None:
            fecha_fin = '2999-01-01'
        
        result = db.session.execute(text('''SELECT SUM(produccion.cantidad) AS cantidad_total,
                                            empleados.nombre, 
                                            empleados.apellido, 
                                            produccion.fecha, 
                                            productos.nombre,
                                            productos.compensacion_unidad, 
                                            productos.compensacion_paquete, 
                                            productos.precio, MAX(roles.nombre) AS nombre_rol
                                            FROM produccion 
                                            JOIN productos ON productos.id_productos = produccion.id_producto
                                            JOIN empleados ON empleados.id_empleados = produccion.id_empleado 
                                            JOIN roles ON roles.id_rol = empleados.id_rol
                                            WHERE empleados.id_empleados = :id_empleado AND produccion.fecha BETWEEN :fecha_inicio AND :fecha_fin
                                            GROUP BY empleados.nombre, empleados.apellido, produccion.fecha, productos.nombre, productos.id_productos;'''), {'id_empleado': id_empleado, 'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin})
        
        schema = ProduccionEmpleadoSchema(many=True)
        produccion_total = schema.dump(result)

        objeto_produccion_empelado = {}
        object_package = []

        for produccion in produccion_total:
            produccion['compensacion_unidad']= float(produccion['compensacion_unidad'])
            produccion['compensacion_paquete']= float(produccion['compensacion_paquete'])
            produccion['cantidad_total']= int(produccion['cantidad_total'])
            produccion['fecha']= str(produccion['fecha'])
            produccion['precio']= int(produccion['precio'])

            ProduccionEmpleado.objeto_final_build(produccion,object_package,objeto_produccion_empelado)
            objeto_produccion_empelado['compensacion_total'] = sum([x['compensacion'] for x in object_package])
        
        return objeto_produccion_empelado
    
    def Total(fecha_inicio,fecha_fin):
        if fecha_inicio == None:
            fecha_inicio = '1999-01-01'
        
        if fecha_fin == None:
            fecha_fin = '2999-01-01'
        
        result = db.session.execute(text('''SELECT SUM(produccion.cantidad) AS cantidad_total,
                                         empleados.nombre,
                                         empleados.apellido,
                                         produccion.fecha,
                                         productos.nombre,
                                         productos.compensacion_unidad,
                                         productos.compensacion_paquete,
                                         productos.precio,
                                         roles.nombre AS nombre_rol

                                         FROM produccion
                                         JOIN productos ON productos.id_productos = produccion.id_producto
                                         JOIN empleados ON empleados.id_empleados = produccion.id_empleado
                                         JOIN roles ON roles.id_rol = empleados.id_rol
                                         WHERE produccion.fecha BETWEEN :fecha_inicio AND :fecha_fin

                                         GROUP BY empleados.nombre, empleados.apellido, produccion.fecha, productos.nombre, productos.id_productos, roles.nombre ;'''), {'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin})
        
        
        schema = ProduccionEmpleadoSchema(many=True)
        produccion_total = schema.dump(result)

        objeto_produccion_empelado = {}
        object_package = []

        for produccion in produccion_total:
        
            ProduccionEmpleado.objeto_final_build(produccion,object_package,objeto_produccion_empelado)
        
        return objeto_produccion_empelado

    

class ProduccionEmpleadoSchema(ma.Schema):
    id_produccion_empleado = fields.Integer(allow_none=False)
    nombre = fields.Str(required=True, allow_none=False)
    apellido = fields.Str(required=True, allow_none=False)
    nombre_producto = fields.Str(required=True, allow_none=False)
    compensacion_unidad = fields.Float(required=True, allow_none=False)
    compensacion_paquete = fields.Float(required=True, allow_none=False)
    cantidad_total = fields.Integer(required=True, allow_none=False)
    fecha = fields.DateTime(required=True, allow_none=False)
    precio = fields.Integer(required=True, allow_none=False)


    class Meta:
        fields = ('id_produccion_empleado', 'nombre', 'apellido', 'nombre_producto', 'compensacion_unidad', 'compensacion_paquete', 'cantidad_total', 'fecha', 'precio')