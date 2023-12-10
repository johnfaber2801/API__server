from setup import db, ma

class User(db.Model):
    # define the table name for the db
    __tablename__= "users"
    # Set the primary key, we need to define that each attribute is also a column in the db table
    id = db.Column(db.Integer,primary_key=True)
    # rest of the attributes.
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

#Use marshmallow to serialize the fields in the model ( we can chooce the fields that we want)
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'username', 'password', 'is_admin')