from sqlalchemy import func
from extensions import db
from models import Score, User, Tournament


def get_tournament_leaderboard(tournament_id: int):
    """
    Generate leaderboard for a tournament.
    Returns:
        (success: bool, message: str, data: dict | None)
    """
    tournament = Tournament.query.get(tournament_id)
    if not tournament:
        return False, "Tournament not found", None

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

    return True, "Leaderboard generated", {
        "tournament": {
            "id": tournament.id,
            "name": tournament.name,
            "status": tournament.status
        },
        "leaderboard": leaderboard
    }
