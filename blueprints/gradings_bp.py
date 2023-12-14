from flask import Blueprint, request, jsonify
from setup import db
from models.grading import Grading, GradingSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.card import Card

gradings_bp = Blueprint('gradings', __name__, url_prefix='/gradings')

#get all graded cards per user
@gradings_bp.route('/')
@jwt_required()
def all_gradings():
    # getting the Jwt token from log in
    user_id = get_jwt_identity() 
    # Query cards owned by the user
    user_cards = Card.query.filter_by(user_id=user_id).all()
     # Extract card IDs
    card_ids = [card.id for card in user_cards]
    # Query gradings associated with those card IDs
    user_gradings = Grading.query.filter(Grading.card_id.in_(card_ids)).all()
    
    return GradingSchema(many=True).dump(user_gradings)
                                 # "dump" will return the fields in JSON format 

#create a Grading for an existing card
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

#Get one graded card
@gradings_bp.route('/<int:id>')
@jwt_required()
def one_graded_card(id):
    user_id = get_jwt_identity()
    stmt = db.select(Grading).filter(Grading.id == id, Grading.card.has(Card.user_id == user_id)) 
    card = db.session.scalar(stmt) 
    if card:
        return GradingSchema().dump(card)
    else:
        return { 'error' : 'Graded card not found' },404
    

# Update graded card
@gradings_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_graded_card(id):
    user_id = get_jwt_identity()
    grading_info = GradingSchema(exclude=['id']).load(request.json)
    stmt = db.select(Grading).filter((Grading.id == id), (Grading.card.has(Card.user_id == user_id)))
    grading = db.session.scalar(stmt)

    if grading:  # If the grading entry is found
        grading.score = grading_info.get('score', grading.score)
        grading.graded_by = grading_info.get('graded_by', grading.graded_by)
        grading.certification = grading_info.get('certification', grading.certification)

        db.session.commit()
        return GradingSchema().dump(grading)
    else:
        return {'error': 'Grading not found'}, 404

    

# Delete one grading
@gradings_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_grading(id):
    user_id = get_jwt_identity()
    stmt = db.select(Grading).filter((Grading.id == id), (Grading.card.has(Card.user_id == user_id))) 
    grading = db.session.scalar(stmt)
    
    if grading:
        db.session.delete(grading)
        db.session.commit()
        return { 'success' : 'Grading was deleted'}, 200
    else:
        return { 'error' : 'Grading details not found or unauthorized' }, 404



