from flask import Blueprint, request, jsonify
from setup import db
from models.grading import Grading, GradingSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.card import Card

gradings_bp = Blueprint('gradings', __name__, url_prefix='/gradings')

@gradings_bp.route('/')
@jwt_required()
def all_gradings():
    stmt= db.select(Grading) # select all users from Grading Model
    gradings = db.session.scalars(stmt).all()
    return GradingSchema(many=True).dump(gradings)
                                 # "dump" will return the fields in JSON format 

@gradings_bp.route('/create/<int:card_id>', methods=['POST'])
@jwt_required()
def create_grading_for_card(card_id):
    # Check if the card exists
    card = Card.query.get(card_id)
    if not card:
        return jsonify({'error': 'Card not found'}), 404

    # Get the user_id from the current JWT token
    user_id = get_jwt_identity()

    # Check if the authenticated user owns the card
    if card.user_id != user_id:
        return jsonify({'error': 'Unauthorized. You do not own this card'}), 403

    grading_info = GradingSchema(exclude=['id']).load(request.json)
    
    grading = Grading(
        score=grading_info.get('score', ''),
        graded_by=grading_info.get('graded_by', ''),
        certification=grading_info.get('certification', ''),
        card_id=card_id
    )

    db.session.add(grading)
    db.session.commit()

    return GradingSchema().dump(grading), 201

# #Get one graded card
# @gradings_bp.route('/<int:id>')
# @jwt_required()
# def one_collection(id):
#     stmt = db.select(Grading).filter_by(id=id) 
#     card = db.session.scalar(stmt)
#     if card:
#         return GradingSchema().dump(card)
#     else:
#         return { 'error' : 'Graded card not found' },404
    
# #create a graded for a card 
# @gradings_bp.route('/', methods=['POST'])
# @jwt_required()
# def create_card():
#     card_info =  GradingSchema(exclude=['id']).load(request.json)
#     # using .get to add empty fields for values that are not mandatoryq
#     card = Grading(
#         score = card_info.get('score',''),
#         graded_by = card_info.get('graded_by', ''),
#         certification = card_info.get('certification', ''),
#         #user_id = get_jwt_identity()
#     )
#     #print(card.__dict__)
#     db.session.add(card)
#     db.session.commit()
#     return GradingSchema().dump(card), 201

# #delete one pokemon card
# @gradings_bp.route('/<int:id>', methods=['DELETE'])
# @jwt_required()
# def delete_card(id):
#     stmt = db.select(Grading).filter_by(id=id) # .where(Card.id == id)
#     card = db.session.scalar(stmt)
#     if card:
#         db.session.delete(card)
#         db.session.commit()
#         return { 'success' : 'Grading was deleted'},200
#     else:
#         return { 'error' : ' Graded card details not found' },404

