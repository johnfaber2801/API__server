from setup import db, ma
from datetime import datetime
from marshmallow import fields
from marshmallow.validate import OneOf

VALID_POKEMON_TYPES = ( 'Normal', 'Fire', 'Water', 'Grass', 'Flying', 'Fighting', 'Poison', 'Electric', 'Ground', 'Rock', 'Psychic', 'Ice', 'Bug', 'Ghost', 'Steel', 'Dragon', 'Dark', 'Fairy')
VALID_CARD_CONDITION_TYPES = ('Mint', 'Near Mint', 'lightly Played', 'Moderately Played', 'Heavily Played ', 'Damaged', 'Graded')

class Card(db.Model):
    # define the table name for the db
    __tablename__= "cards"

    # Set the primary key, we need to define that each attribute is also a column in the db table
    id = db.Column(db.Integer,primary_key=True)

    # rest of the attributes.
    name = db.Column(db.String(), nullable= False)
    type = db.Column(db.String(), nullable= False)
    set = db.Column(db.String())
    condition= db.Column(db.String(), nullable= False)
    quantity = db.Column(db.Integer(), nullable= False)
    purchased_price = db.Column(db.Integer())
    market_price = db.Column(db.Integer())
    date = db.Column(db.Date(), default=datetime.now().strftime('%Y-%m-%d'))

    #foreign key                                 #table name in the foreign "User" model
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False)
    #the convention is "_id" for the foreign key              # user_id must have a card "nullable=false"

    #SQLAlchemy relantionship- nests an instance of a related model in this one
    user = db.relationship('User', back_populates= 'cards')
                            #tellin alchemy that this relationship is related to "cards" relationshi in User model
    
    grading = db.relationship('Grading', back_populates='card',  cascade='all, delete-orphan')
                                                                 #will delete user and associated cards.

#Use marshmallow to serialize the fields in the model ( we can chooce the fields that we want)
class CardSchema(ma.Schema):
    #grading = fields.Nested('GradingSchema', exclude=['card_id'], many=True)###3333333333
    user = fields.Nested('UserSchema', exclude=['password', 'is_admin'])###3333333333
    grading = fields.Nested('GradingSchema', exclude=['card'])  # Exclude the circular reference

    type = fields.String(validate=OneOf(VALID_POKEMON_TYPES))
    condition = fields.String(validate=OneOf(VALID_CARD_CONDITION_TYPES))

   #tell marsmallows to pass as well the entire "UserSchema"
    class Meta:                                                                                  #user object from the nested
        fields = ('id', 'name', 'type', 'set', 'condition','quantity', 'purchased_price','market_price', 'date','user')