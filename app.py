from src.setup import app
from src.blueprints.cli_bp import db_commands
from src.blueprints.users_bp import users_bp
from src.blueprints.cards_bp import cards_bp
from src.blueprints.gradings_bp import gradings_bp

#Register blueprints for different parts of the application
app.register_blueprint(db_commands)
app.register_blueprint(users_bp)
app.register_blueprint(cards_bp)
app.register_blueprint(gradings_bp)

#will show all the routes with their maps in the terminal
print( app.url_map) 




