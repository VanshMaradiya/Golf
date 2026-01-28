from flask import Flask
from config import Config
from extensions import db

# 🔹 Import blueprints
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.player_routes import player_bp
from routes.score_routes import score_bp
from routes.leaderboard_routes import leaderboard_bp
from routes.tournament_routes import tournament_bp
from routes.ui_routes import ui_bp


# 🔹 IMPORTANT: Import all models so SQLAlchemy knows them
from models import user, golf_course, hole, tournament, score


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 🔹 Initialize extensions
    db.init_app(app)

    # 🔹 Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(player_bp)
    app.register_blueprint(score_bp)
    app.register_blueprint(leaderboard_bp)
    app.register_blueprint(tournament_bp)
    app.register_blueprint(ui_bp)

    return app


# # 🔹 Create app instance
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)




