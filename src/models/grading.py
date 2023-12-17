from src.setup import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf

VALID_GRADING_COMPANIES = ('PSA', 'BECKETT', 'CGC')

class Grading(db.Model):

    # define the table name for the db
    __tablename__= "gradings"

    # Set the primary key, we need to define that each attribute is also a column in the db table
    id = db.Column(db.Integer,primary_key=True)

    # rest of the attributes.
    score = db.Column(db.String(), nullable=False)
    graded_by = db.Column(db.String(), nullable=False)
    certification = db.Column(db.String(), nullable=False)

 # ForeignKey to relate Grading to Card 
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'), nullable=False)
    card = db.relationship('Card', back_populates='grading')

#Use marshmallow to serialize the fields in the model ( we can chooce the fields that we want)
class GradingSchema(ma.Schema):

    card = fields.Nested('CardSchema', only=['name'])

    #validates the graded_by with the valid list of grading companies
    graded_by = fields.String(validate=OneOf(VALID_GRADING_COMPANIES))
                              
    class Meta:
        fields = ('id', 'score', 'graded_by', 'certification','card')
                                                               