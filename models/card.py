from setup import db, ma

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