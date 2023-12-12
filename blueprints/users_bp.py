from flask import Blueprint, request
from setup import db, bcrypt
from auth import admin_required
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta
from sqlalchemy.exc import IntegrityError
from models.user import User, UserSchema

users_bp = Blueprint('users', __name__, url_prefix='/users')


# Get all users
@users_bp.route('/')
@jwt_required()
def all_users():
    admin_required()
    stmt= db.select(User)# select all cards from User Model
    users = db.session.scalars(stmt).all()
    return UserSchema(many=True,exclude=['password']).dump(users)
                                 # "dump" will return the fields in JSON format                           

# register new users 
@users_bp.route('/register', methods=['POST'])
def register():
    try:
        #parse incoming POST body through the schema
        user_info = UserSchema(exclude=['id','is_admin']).load(request.json)
        #create a new user with the parsed data
        user = User(
            email=user_info['email'],
            username=user_info['username'],
            password=bcrypt.generate_password_hash(user_info['password']).decode('utf8')
        )
        #add and commit the new user to the database
        db.session.add(user)
        db.session.commit()

        #return new user                                  # 201 creation successful
        return UserSchema(exclude=['password','id']).dump(user), 201
                        #password and ID wont be retrieved to new users
    except IntegrityError as e:
        # Check if the error is due to duplicate email
        if 'unique constraint' in str(e.orig) and 'email' in str(e.orig):
            return {'error': 'Email is already in use'}, 409
        # Check if the error is due to duplicate username
        elif 'unique constraint' in str(e.orig) and 'username' in str(e.orig):
            return {'error': 'Username is already in use'}, 409

#login route                
@users_bp.route('/login', methods=['POST'])
def login():
    #parse incoming POST body through the schema
    user_info = UserSchema(only=['email','password']).load(request.json)
    #select user with email that matches the one in the POST body
    stmt = db.select(User).where(User.email==user_info['email'])
    user = db.session.scalar(stmt)  
    #check password hash #bcrypt will do the work for us of matching password from database and incoming one
    if user and bcrypt.check_password_hash(user.password, user_info['password']):
        #create a JWT token
        token = create_access_token(identity=user.id,expires_delta=timedelta(hours=12))
        #return the JWT token
        return {'token': token, 'user':UserSchema(exclude=['password','cards']).dump(user)}
    else:
        return {'error': 'invalid email or password'},401
    


