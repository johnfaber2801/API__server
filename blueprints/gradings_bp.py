from flask import Blueprint
from setup import db
from models.grading import Grading, GradingSchema
from flask_jwt_extended import jwt_required

gradings_bp = Blueprint('gradings', __name__, url_prefix='/gradings')

@gradings_bp.route('/')
def all_gradings():
    stmt= db.select(Grading) # select all users from Grading Model
    gradings = db.session.scalars(stmt).all()
    return GradingSchema(many=True).dump(gradings)
                                 # "dump" will return the fields in JSON format 

#Get one graded card
@gradings_bp.route('/<int:id>')
#@jwt_required()
def one_collection(id):
    stmt = db.select(Grading).filter_by(id=id) 
    card = db.session.scalar(stmt)
    if card:
        return GradingSchema().dump(card)
    else:
        return { 'error' : 'Graded card not found' },404