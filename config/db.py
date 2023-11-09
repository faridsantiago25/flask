from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
app = Flask(__name__)

#creamos las credenciales para conectarnos a la bd
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://farid2504:root1234@farid2504.mysql.pythonanywhere-services.com/farid2504$webDatabase'
app.config['SQLALCHEMY_TRACK_MODIFACATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1

app.secret_key = "mysecretkey"

#creamos los objetos de bd

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)