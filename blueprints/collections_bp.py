from flask import Blueprint ,request
from setup import db
from models.collection import Collection, CollectionSchema
from flask_jwt_extended import jwt_required , get_jwt_identity

collections_bp = Blueprint('collections', __name__, url_prefix='/collections')

#get all collections
@collections_bp.route('/')
@jwt_required()
def all_collections():
    user_id = get_jwt_identity()  
    stmt= db.select(Collection).filter_by(user_id=user_id) # select all users from Grading Model
    collections = db.session.scalars(stmt).all()
    return CollectionSchema(many=True).dump(collections)
                                 # "dump" will return the fields in JSON format 

# #Get one collection
# @collections_bp.route('/<int:id>')
# @jwt_required()
# def one_collection(id):
#     user_id = get_jwt_identity()
#     stmt = db.select(Collection).filter_by(id=id, user_id=user_id) 
#     card = db.session.scalar(stmt)
#     if card:
#         return CollectionSchema().dump(card)
#     else:
#         return { 'error' : 'Collection not found' },404
    
# #create a new pokemon card
# @collections_bp.route('/', methods=['POST'])
# @jwt_required()
# def create_card():
#     collection_info =  CollectionSchema(exclude=['id']).load(request.json)
#     # using .get to add empty fields for values that are not mandatoryq
#     collection = Collection(
#         collection_name = collection_info.get('collection_name',''),
#         #user_id = get_jwt_identity()
#     )
#     #print(card.__dict__)
#     db.session.add(collection)
#     db.session.commit()
#     return CollectionSchema().dump(collection), 201

# #update pokemon card
# @collections_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
# @jwt_required()
# def update_card(id):
#     collection_info =  CollectionSchema(exclude=['id']).load(request.json)
#     stmt = db.select(Collection).filter_by(id=id) # .where(Card.id == id)
#     collection = db.session.scalar(stmt)
#     if collection:  # if field is not updated, it will keep the existing one
#         collection.collection_name = collection_info.get('collection_name', collection.collection_name)
#         db.session.commit()       
#         return CollectionSchema().dump(collection)
#     else:
#         return { 'error' : 'Card not found' },404
    

# #delete one pokemon card
# @cards_bp.route('/<int:id>', methods=['DELETE'])
# @jwt_required()
# def delete_card(id):
#     stmt = db.select(Card).filter_by(id=id) # .where(Card.id == id)
#     card = db.session.scalar(stmt)
#     if card:
#         db.session.delete(card)
#         db.session.commit()
#         return { 'success' : 'pokemon card was deleted'},200
#     else:
#         return { 'error' : 'Card not found' },404