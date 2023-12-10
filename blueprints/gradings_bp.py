from flask import Blueprint
from setup import db
from models.grading import Grading, GradingSchema

gradings_bp = Blueprint('gradings', __name__, url_prefix='/gradings')

@gradings_bp.route('/')
def all_gradings():
    stmt= db.select(Grading) # select all users from Grading Model
    gradings = db.session.scalars(stmt).all()
    return GradingSchema(many=True).dump(gradings)
                                 # "dump" will return the fields in JSON format 