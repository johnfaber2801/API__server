from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from datetime import date
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow

app = Flask(__name__)
# set the database URI via SQLAlchemy, 
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://pokemon_dev:123456@localhost:5432/pokemon_db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#create the database object
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
ma = Marshmallow(app)

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
        fields = ('id', 'email', 'username', 'password')


@app.route('/users')
def all_users():
    stmt= db.select(User)
    users = db.session.scalars(stmt).all()
    return UserSchema(many=True).dump(users)
                                 # "dump" will return the fields in JSON format 


class Card(db.Model):
    # define the table name for the db
    __tablename__= "cards"
    # Set the primary key, we need to define that each attribute is also a column in the db table
    id = db.Column(db.Integer,primary_key=True)
    # rest of the attributes.
    name = db.Column(db.String(), nullable= False)
    type = db.Column(db.String())
    set = db.Column(db.String())
    condition= db.Column(db.String())
    quantity = db.Column(db.Integer(), nullable= False)
    purchased_price = db.Column(db.Integer())
    market_price = db.Column(db.Integer())
    date = db.Column(db.Date())

#Use marshmallow to serialize the fields in the model ( we can chooce the fields that we want)
class CardSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'type', 'set', 'description', 'purchased_price','market_price', 'date')


@app.route('/cards')
def all_cards():
    stmt= db.select(Card)# select all cards from Card Model
    cards = db.session.scalars(stmt).all()
    return CardSchema(many=True).dump(cards)
                                 # "dump" will return the fields in JSON format   

class Grading(db.Model):
    # define the table name for the db
    __tablename__= "gradings"
    # Set the primary key, we need to define that each attribute is also a column in the db table
    id = db.Column(db.Integer,primary_key=True)
    # rest of the attributes.
    score = db.Column(db.String(), nullable=False)
    graded_by = db.Column(db.String(), nullable=False)
    certification = db.Column(db.String(), nullable=False)

#Use marshmallow to serialize the fields in the model ( we can chooce the fields that we want)
class GradingSchema(ma.Schema):
    class Meta:
        fields = ('id', 'score', 'graded_by', 'certifcation')


@app.route('/gradings')
def all_gradings():
    stmt= db.select(Grading) # select all users from Grading Model
    gradings = db.session.scalars(stmt).all()
    return GradingSchema(many=True).dump(gradings)
                                 # "dump" will return the fields in JSON format 

class Collection(db.Model):
    # define the table name for the db
    __tablename__= "collections"
    # Set the primary key, we need to define that each attribute is also a column in the db table
    id = db.Column(db.Integer,primary_key=True)
    # rest of the attributes.
    collection_name= db.Column(db.String())

#Use marshmallow to serialize the fields in the model ( we can chooce the fields that we want)
class CollectionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'collection_name')


@app.route('/collections')
def all_collections():
    stmt= db.select(Collection) # select all users from Grading Model
    collections = db.session.scalars(stmt).all()
    return CollectionSchema(many=True).dump(collections)
                                 # "dump" will return the fields in JSON format 

@app.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")

@app.cli.command("seed")
def db_seed():
    # Users 
    cards = [
         Card(
            name = "Charizard #1",
            type = "fire",
            set = "25th Anniversary promo",
            condition= "near mint",
            quantity = 1,
            purchased_price = 180,
            market_price = 195,
            date = date.today()
        ),
    # db.session.add(card1)

          Card(
            name = "Imposter Professor Oak #4",
            type = "Trainer",
            set = "25th Anniversary promo",
            condition= "Little played",
            quantity = 1,
            purchased_price = 4,
            market_price = 5.5,
            date = date.today()
        )
    ]
    # db.session.add(card2)
    db.session.add_all(cards)
    db.session.commit()

    users =[
        User(
            email="admin@spam.com",
            username="jefe",
            password=bcrypt.generate_password_hash("spinynorman").decode("utf8"),
            is_admin=True,
        ),
    #db.session.add(user1)

        User(
            email="rodriguez@spam.com",
            username="collector2023",
            password=bcrypt.generate_password_hash("tisbutascratch").decode("utf8"),
        )
    ]

    db.session.add_all(users)
    db.session.commit()
    #db.session.add(user2)

    collections = [
        Collection (
        collection_name = " Japanese pokemon card sets"   
    )
    ]
    db.session.add_all(collections)
    db.session.commit()

    gradings = [
        Grading(
        score = 9,
        graded_by = "PSA",
        certification = 9865649741        
    ),
    Grading(
        score = 10,
        graded_by = "Beckett",
        certification = 5951654565       
    )
    ] 
    db.session.add_all(gradings)
    db.session.commit()

    print("Database seeded")


@app.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped") 


    


@app.route("/")
def hello():
  return "Hello World!"