from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.player_routes import player_bp
from routes.score_routes import score_bp
from routes.leaderboard_routes import leaderboard_bp
from routes.tournament_routes import tournament_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(player_bp)
    app.register_blueprint(score_bp)
    app.register_blueprint(leaderboard_bp)
    app.register_blueprint(tournament_bp)