from flask import Blueprint, request, jsonify
from models import Tournament, Score

player_bp = Blueprint("player", __name__, url_prefix="/api/player")


# ---------------------------
# VIEW TOURNAMENTS
# ---------------------------
@player_bp.route("/tournaments", methods=["GET"])
def view_tournaments():
    tournaments = Tournament.query.all()

    return jsonify([
        {
            "id": t.id,
            "name": t.name,
            "status": t.status
        }
        for t in tournaments
    ]), 200


# ---------------------------
# JOIN TOURNAMENT (NO DB INSERT)
# ---------------------------
@player_bp.route("/tournaments/<int:tournament_id>/join", methods=["POST"])
def join_tournament(tournament_id):
    user_id = request.headers.get("X-User-Id")

    if not user_id:
        return jsonify({"error": "X-User-Id header required"}), 401

    tournament = Tournament.query.get_or_404(tournament_id)

    # Optional: check if already has any score in this tournament
    already_joined = Score.query.filter_by(
        user_id=int(user_id),
        tournament_id=tournament_id
    ).first()

    if already_joined:
        return jsonify({"error": "Already joined"}), 409

    return jsonify({
        "message": "Tournament joined successfully",
        "tournament": {
            "id": tournament.id,
            "name": tournament.name,
            "status": tournament.status
        }
    }), 200


# ---------------------------
# VIEW ALL MY SCORES
# ---------------------------
@player_bp.route("/my-scores", methods=["GET"])
def my_scores():
    user_id = request.headers.get("X-User-Id")

    if not user_id:
        return jsonify({"error": "X-User-Id header required"}), 401

    scores = Score.query.filter_by(user_id=int(user_id)).all()

    return jsonify([
        {
            "tournament_id": s.tournament_id,
            "hole_id": s.hole_id,
            "strokes": s.strokes
        }
        for s in scores
    ]), 200
