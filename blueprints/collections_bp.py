from flask import Blueprint
from setup import db
from models.collection import Collection, CollectionSchema

collections_bp = Blueprint('collections', __name__, url_prefix='/collections')


@collections_bp.route('/')
def all_collections():
    stmt= db.select(Collection) # select all users from Grading Model
    collections = db.session.scalars(stmt).all()
    return CollectionSchema(many=True).dump(collections)
                                 # "dump" will return the fields in JSON format 