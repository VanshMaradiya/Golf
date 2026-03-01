from datetime import datetime
from extensions import db


class Hole(db.Model):
    __tablename__ = "holes"

    id = db.Column(db.Integer, primary_key=True)

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("golf_courses.id", ondelete="CASCADE"),
        nullable=False
    )

    hole_number = db.Column(db.Integer, nullable=False)
    par = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint(
            "course_id",
            "hole_number",
            name="unique_hole_per_course"
        ),
    )

    def __repr__(self):
        return f"<Hole {self.hole_number} (Course {self.course_id})>"
