from flask import Flask
from os import environ
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')

# set the database URI via SQLAlchemy, 
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DB_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#create the database object
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
    
#it wil handle access denied from not admin users    
@app.errorhandler(401)
def unauthorized(err):
    return {'error':'You are not authrorized to access this resource'}