from datetime import datetime
from extensions import db


class Score(db.Model):
    __tablename__ = "scores"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    tournament_id = db.Column(
        db.Integer,
        db.ForeignKey("tournaments.id", ondelete="CASCADE"),
        nullable=False
    )

    hole_id = db.Column(
        db.Integer,
        db.ForeignKey("holes.id", ondelete="CASCADE"),
        nullable=False
    )

    strokes = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="scores")
    hole = db.relationship("Hole", backref="scores")

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "tournament_id",
            "hole_id",
            name="unique_score_per_hole"
        ),
    )

    def __repr__(self):
        return (
            f"<Score User:{self.user_id} "
            f"Tournament:{self.tournament_id} "
            f"Hole:{self.hole_id} "
            f"Strokes:{self.strokes}>"
        )
