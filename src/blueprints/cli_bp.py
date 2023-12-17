from flask import Blueprint
from src.setup import db, bcrypt
from src.models.user import User
from src.models.grading import Grading
from src.models.card import Card
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

    # cards 
    cards = [
         Card(
            name = "Charizard #1",
            type = "Fire",
            set = "25th Anniversary promo",
            condition= "Graded",
            quantity = 1,
            purchased_price = 180,
            market_price = 195,
            date = date.today(),
            user_id = users[0].id
        ),

          Card(
            name = "Imposter Professor Oak #4",
            type = "Normal",
            set = "25th Anniversary promo",
            condition= "Graded",
            quantity = 1,
            purchased_price = 4,
            market_price = 5.5,
            date = date.today(),
            user_id = users[1].id
        )
    ]
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
        graded_by = "BECKETT",
        certification = 5951654565,
        card_id=cards[1].id        
    )
    ] 
    db.session.add_all(gradings)
    db.session.commit()
  

    print("Database seeded")


@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped") 