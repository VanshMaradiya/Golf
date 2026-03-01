from datetime import datetime
from extensions import db

class GolfCourse(db.Model):
    __tablename__ = "golf_courses"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False, unique=True)
    location = db.Column(db.String(150), nullable=False)

    total_holes = db.Column(db.Integer, nullable=False, default=18)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    holes = db.relationship(
        "Hole",
        backref="course",
        lazy=True,
        cascade="all, delete-orphan"
    )

    tournaments = db.relationship(
        "Tournament",
        backref="course",
        lazy=True
    )

    def __repr__(self):
        return f"<GolfCourse {self.name}>"
