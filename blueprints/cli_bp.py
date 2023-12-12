from flask import Blueprint
from setup import db, bcrypt
from models.user import User
from models.grading import Grading
from models.collection import Collection
from models.card import Card
from datetime import date

#instance creation from blueprint
db_commands = Blueprint('db', __name__)

@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")

@db_commands.cli.command("seed")
def db_seed():
    #users
    users =[
        User(
            email="admin@spam.com",
            username="jefe",
            password=bcrypt.generate_password_hash("spinynorman").decode("utf8"),
            is_admin=True,   #industry standars of how to store a password.
        ),
    #db.session.add(user1)

        User(
            email="rodriguez@spam.com",
            username="collector2023",
            password=bcrypt.generate_password_hash("tisbutascratch").decode("utf8"),
        )                  #industry standars of how to store a password.               
    ]

    db.session.add_all(users)
    db.session.commit()
    #db.session.add(user2)

    # cards 
    cards = [
         Card(
            name = "Charizard #1",
            type = "fire",
            set = "25th Anniversary promo",
            condition= "near mint",
            quantity = 1,
            purchased_price = 180,
            market_price = 195,
            date = date.today(),
            user_id = users[0].id
        ),
    # db.session.add(card1)

          Card(
            name = "Imposter Professor Oak #4",
            type = "Trainer",
            set = "25th Anniversary promo",
            condition= "Little played",
            quantity = 1,
            purchased_price = 4,
            market_price = 5.5,
            date = date.today(),
            user_id = users[1].id
        )
    ]
    # db.session.add(card2)
    db.session.add_all(cards)
    db.session.commit()

    #graded card sets
    gradings = [
        Grading(
        score = 9,
        graded_by = "PSA",
        certification = 9865649741,
        card_id=cards[0].id       
    ),
    Grading(
        score = 10,
        graded_by = "Beckett",
        certification = 5951654565,
        card_id=cards[1].id        
    )
    ] 
    db.session.add_all(gradings)
    db.session.commit()

    #collections
    collections = [
        Collection (
        collection_name = " Japanese pokemon card sets"   
    )
    ]
    db.session.add_all(collections)
    db.session.commit()

    

    print("Database seeded")


@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped") 