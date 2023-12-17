from flask import Flask
from os import environ
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from marshmallow.exceptions import ValidationError

# Create a Flask app instance   
app = Flask(__name__)

# Set the JWT secret key
app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')

# set the database URI via SQLAlchemy, 
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DB_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# creating our database object! This allows us to use our ORM
db = SQLAlchemy(app)

# creating our marshmallow object! This allows us to use schemas
ma = Marshmallow(app)

#creating the jwt and bcrypt objects! this allows us to use authentication
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


    
#it will handle access denied from not admin users    
@app.errorhandler(401)
def unauthorized(err):
    return {'error':'You are not authrorized to access this resource'}

@app.errorhandler(ValidationError)
def validation_error(err):
    return {'error': err.messages}