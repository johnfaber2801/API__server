from setup import db, ma
from marshmallow import fields

class Grading(db.Model):
    # define the table name for the db
    __tablename__= "gradings"
    # Set the primary key, we need to define that each attribute is also a column in the db table
    id = db.Column(db.Integer,primary_key=True)
    # rest of the attributes.
    score = db.Column(db.String(), nullable=False)
    graded_by = db.Column(db.String(), nullable=False)
    certification = db.Column(db.String(), nullable=False)

 # ForeignKey to relate Grading to Card 333333333333333333333333333
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'), nullable=False)
    card = db.relationship('Card', back_populates='grading')

#Use marshmallow to serialize the fields in the model ( we can chooce the fields that we want)
class GradingSchema(ma.Schema):
    class Meta:
        fields = ('id', 'score', 'graded_by', 'certification','card_id')
                                                                ########