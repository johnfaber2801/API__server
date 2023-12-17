from src.setup import db, ma
from marshmallow import fields
from marshmallow.validate import Length

class User(db.Model):

    # define the table name for the db
    __tablename__= "users"

    # the primary key
    id = db.Column(db.Integer,primary_key=True)

    # rest of the attributes.
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    #telling alchemy that this relationship is related to "user" relationship in User model
    cards = db.relationship('Card', back_populates='user',  cascade='all, delete-orphan')
                               
#Use marshmallow to serialize the fields in the model ( we can chooce the fields that we want)
class UserSchema(ma.Schema):

    cards = fields.Nested('CardSchema', exclude=['user'], many=True)

    #validates the email
    email = fields.Email (required=True) 
    #validates the password
    password = fields.String (required=True, validate=Length(min=6, error='Password must be at least 6 characters')) 
    
    class Meta:
        fields = ('id', 'email', 'username', 'password', 'is_admin', 'cards')