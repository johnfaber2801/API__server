from setup import app
from blueprints.cli_bp import db_commands
from blueprints.users_bp import users_bp
from blueprints.cards_bp import cards_bp
from blueprints.gradings_bp import gradings_bp
from blueprints.collections_bp import collections_bp


app.register_blueprint(db_commands)
app.register_blueprint(users_bp)
app.register_blueprint(cards_bp)
app.register_blueprint(gradings_bp)
app.register_blueprint(collections_bp)



