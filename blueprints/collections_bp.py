from flask import Blueprint
from setup import db
from models.collection import Collection, CollectionSchema
from flask_jwt_extended import jwt_required

collections_bp = Blueprint('collections', __name__, url_prefix='/collections')

#get all collections
@collections_bp.route('/')
def all_collections():
    stmt= db.select(Collection) # select all users from Grading Model
    collections = db.session.scalars(stmt).all()
    return CollectionSchema(many=True).dump(collections)
                                 # "dump" will return the fields in JSON format 

#Get one collection
@collections_bp.route('/<int:id>')
#@jwt_required()
def one_collection(id):
    stmt = db.select(Collection).filter_by(id=id) 
    card = db.session.scalar(stmt)
    if card:
        return CollectionSchema().dump(card)
    else:
        return { 'error' : 'Collection not found' },404