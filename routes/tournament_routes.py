from flask import Blueprint, request, jsonify
from extensions import db
from models import Tournament, GolfCourse
from datetime import datetime

tournament_bp = Blueprint("tournament", __name__, url_prefix="/api/tournaments")


def admin_required():
    role = request.headers.get("X-User-Role")
    if role != "admin":
        return jsonify({"error": "Admin access required"}), 403


# CREATE TOURNAMENT (ADMIN)

@tournament_bp.route("", methods=["POST"])
def create_tournament():
    auth = admin_required()
    if auth:
        return auth

    data = request.get_json() or {}

    name = data.get("name")
    course_id = data.get("course_id")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    if not all([name, course_id, start_date, end_date]):
        return jsonify({
            "error": "name, course_id, start_date, end_date are required"
        }), 400

    course = GolfCourse.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    # FORCE ongoing 
    tournament = Tournament(
        name=name,
        course_id=course_id,
        start_date=datetime.fromisoformat(start_date),
        end_date=datetime.fromisoformat(end_date),
        status="ongoing"
    )

    db.session.add(tournament)
    db.session.commit()

    return jsonify({
        "message": "Tournament created successfully",
        "tournament_id": tournament.id,
        "status": "ongoing"
    }), 201
