from flask import Blueprint, request
from setup import db
from models.card import Card, CardSchema
from flask_jwt_extended import jwt_required

cards_bp = Blueprint('cards', __name__, url_prefix='/cards')

# Get all cards
@cards_bp.route('/')
#@jwt_required()
def all_cards():
    stmt= db.select(Card)# select all cards from Card Model
    cards = db.session.scalars(stmt).all()
    return CardSchema(many=True).dump(cards)
                                 # "dump" will return the fields in JSON format   


#Get one card
@cards_bp.route('/<int:id>')
#@jwt_required()
def one_card(id):
    stmt = db.select(Card).filter_by(id=id) # .where(Card.id == id)
    card = db.session.scalar(stmt)
    if card:
        return CardSchema().dump(card)
    else:
        return { 'error' : 'Card not found' },404
    
#create a new pokemon card
@cards_bp.route('/', methods=['POST'])
def create_card():
    card_info =  CardSchema(exclude=['id','date']).load(request.json)
    # using .get to add empty fields for values that are not mandatoryq
    card = Card(
        name = card_info['name'],
        type = card_info.get('type'),
        set = card_info.get('set',''),
        condition = card_info.get('condition',''),
        quantity = card_info['quantity'],
        purchased_price = card_info.get('purchased_price',''),
        market_price = card_info.get('market_price','')
    )
    #print(card.__dict__)
    db.session.add(card)
    db.session.commit()
    return CardSchema().dump(card), 201

#update pokemon card
@cards_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update_card(id):
    card_info =  CardSchema(exclude=['id','date']).load(request.json)
    stmt = db.select(Card).filter_by(id=id) # .where(Card.id == id)
    card = db.session.scalar(stmt)
    if card:  # if field is not updated, it will keep the existing one
        card.name = card_info.get('name', card.name)
        card.type = card_info.get('type', card.type)
        card.set = card_info.get('set', card.set)
        card.condition = card_info.get('description',card.condition)
        card.quantity = card_info.get('quantity', card.quantity)
        card.purchased_price = card_info.get('purchased_price', card.purchased_price)
        card.market_price = card_info.get('market_price', card.market_price)
        db.session.commit()       
        return CardSchema().dump(card)
    else:
        return { 'error' : 'Card not found' },404
    

#delete one pokemon card
@cards_bp.route('/<int:id>', methods=['DELETE'])
#@jwt_required()
def delete_card(id):
    stmt = db.select(Card).filter_by(id=id) # .where(Card.id == id)
    card = db.session.scalar(stmt)
    if card:
        db.session.delete(card)
        db.session.commit()
        return { 'success' : 'pokemon card was deleted'},200
    else:
        return { 'error' : 'Card not found' },404


