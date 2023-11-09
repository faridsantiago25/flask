from config.db import app, db, ma
from marshmallow import fields, ValidationError
from validations.valitadions import validate_str
from sqlalchemy import text


class Roles(db.Model):
    _tabllename_ = 'roles'
    id_rol = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(45))

    def __init__(self,nombre):
        self.nombre = nombre

with app.app_context():
    db.create_all()


def validar_nombre(val):
    val = val.lower()
    raw_query = text("SELECT * FROM roles WHERE LOWER(nombre) nombre = :nombre")
    params = {"nombre":val}

    existing_role = db.session.execute(raw_query, params)
    row = existing_role.fetchone()

    if row[0] == 1:
        raise ValidationError("El rol ya existe")

class RolesSchema(ma.Schema):
    id_rol = fields.Integer(allow_none=False)
    nombre = fields.Str(required=True, allow_none=False, validate=[validate_str, validar_nombre])

    class Meta:
        fields = ('id_rol', 'nombre')