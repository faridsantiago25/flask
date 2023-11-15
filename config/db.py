from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
import os
app = Flask(__name__)

#creamos las credenciales para conectarnos a la bd
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")
app.config['SQLALCHEMY_TRACK_MODIFACATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1

app.secret_key = "mysecretkey"

#creamos los objetos de bd

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)