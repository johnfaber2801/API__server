from setup import db, ma

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