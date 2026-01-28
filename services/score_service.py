from models import Score, Tournament, Hole, User
from extensions import db


def add_or_update_score(user_id: int, tournament_id: int, hole_id: int, strokes: int):
    """
    Add or update a score for a user in a tournament hole
    """

    # --------------------
    # Validate user
    # --------------------
    user = User.query.get(user_id)
    if not user:
        return False, "User not found"

    # --------------------
    # Validate tournament
    # --------------------
    tournament = Tournament.query.get(tournament_id)
    if not tournament:
        return False, "Tournament not found"

    if tournament.status != "ongoing":
        return False, "Tournament is not ongoing"

    # --------------------
    # Validate hole
    # --------------------
    hole = Hole.query.get(hole_id)
    if not hole:
        return False, "Hole not found"

    # Ensure hole belongs to the tournament course
    if hole.course_id != tournament.course_id:
        return False, "Hole does not belong to this tournament"

    # --------------------
    # Add or update score
    # --------------------
    try:
        score = Score.query.filter_by(
            user_id=user_id,
            tournament_id=tournament_id,
            hole_id=hole_id
        ).first()

        if score:
            score.strokes = strokes
            message = "Score updated successfully"
        else:
            score = Score(
                user_id=user_id,
                tournament_id=tournament_id,
                hole_id=hole_id,
                strokes=strokes
            )
            db.session.add(score)
            message = "Score added successfully"

        db.session.commit()
        return True, message

    except Exception as e:
        db.session.rollback()
        return False, "Failed to save score"


def get_user_scores(user_id: int, tournament_id: int):
    """
    Get all scores of a user for a tournament
    """

    # Validate user
    user = User.query.get(user_id)
    if not user:
        return False, "User not found"

    # Validate tournament
    tournament = Tournament.query.get(tournament_id)
    if not tournament:
        return False, "Tournament not found"

    scores = Score.query.filter_by(
        user_id=user_id,
        tournament_id=tournament_id
    ).order_by(Score.hole_id.asc()).all()

    return True, {
        "user_id": user_id,
        "tournament_id": tournament_id,
        "scores": [
            {
                "hole_id": score.hole_id,
                "strokes": score.strokes
            }
            for score in scores
        ]
    }
