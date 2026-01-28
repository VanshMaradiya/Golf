from flask import Blueprint, jsonify
from sqlalchemy import func
from extensions import db
from models import Score, User, Tournament

leaderboard_bp = Blueprint(
    "leaderboard",
    __name__,
    url_prefix="/api/leaderboard"
)


# ---------------------------
# TOURNAMENT LEADERBOARD
# ---------------------------
@leaderboard_bp.route("/tournaments/<int:tournament_id>", methods=["GET"])
def tournament_leaderboard(tournament_id):
    # Validate tournament existence
    tournament = Tournament.query.get_or_404(tournament_id)

    # Aggregate total strokes per player
    results = (
        db.session.query(
            User.id.label("user_id"),
            User.name.label("player_name"),
            func.coalesce(func.sum(Score.strokes), 0).label("total_strokes")
        )
        .join(Score, Score.user_id == User.id)
        .filter(Score.tournament_id == tournament_id)
        .group_by(User.id, User.name)
        .order_by(func.coalesce(func.sum(Score.strokes), 0))
        .all()
    )

    leaderboard = []
    rank = 1

    for row in results:
        leaderboard.append({
            "rank": rank,
            "user_id": row.user_id,
            "player_name": row.player_name,
            "total_strokes": int(row.total_strokes)
        })
        rank += 1

    return jsonify({
        "tournament": {
            "id": tournament.id,
            "name": tournament.name,
            "status": tournament.status
        },
        "leaderboard": leaderboard
    }), 200
