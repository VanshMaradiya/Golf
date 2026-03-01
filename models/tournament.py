from datetime import datetime
from extensions import db


class Tournament(db.Model):
    __tablename__ = "tournaments"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("golf_courses.id", ondelete="RESTRICT"),
        nullable=False
    )

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    status = db.Column(
        db.String(30),
        default="upcoming"
    )  # upcoming, ongoing, completed

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    scores = db.relationship(
        "Score",
        backref="tournament",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Tournament {self.name} ({self.status})>"
