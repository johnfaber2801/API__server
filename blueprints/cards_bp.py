from flask import Blueprint
from setup import db
from models.card import Card, CardSchema

cards_bp = Blueprint('cards', __name__, url_prefix='/cards')

@cards_bp.route('/')
#@jwt_required()
def all_cards():
    stmt= db.select(Card)# select all cards from Card Model
    cards = db.session.scalars(stmt).all()
    return CardSchema(many=True).dump(cards)
                                 # "dump" will return the fields in JSON format   