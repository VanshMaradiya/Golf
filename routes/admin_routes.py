from flask import Blueprint, request, jsonify
from extensions import db
from models import GolfCourse, Hole
from utils.permissions import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


# -------------------------
# CREATE GOLF COURSE
# -------------------------
@admin_bp.route("/courses", methods=["POST"])
@admin_required
def create_course():
    data = request.get_json() or {}

    name = data.get("name")
    location = data.get("location")
    total_holes = data.get("total_holes", 18)

    if not name or not location:
        return jsonify({"error": "Name and location required"}), 400

    if GolfCourse.query.filter_by(name=name).first():
        return jsonify({"error": "Course already exists"}), 409

    course = GolfCourse(
        name=name,
        location=location,
        total_holes=total_holes
    )

    db.session.add(course)
    db.session.commit()

    return jsonify({
        "message": "Golf course created successfully",
        "course_id": course.id
    }), 201


# -------------------------
# GET ALL COURSES (PUBLIC)
# -------------------------
@admin_bp.route("/courses", methods=["GET"])
def get_courses():
    courses = GolfCourse.query.all()

    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "location": c.location,
            "total_holes": c.total_holes
        }
        for c in courses
    ]), 200


# -------------------------
# ADD HOLE
# -------------------------
@admin_bp.route("/courses/<int:course_id>/holes", methods=["POST"])
@admin_required
def add_hole(course_id):
    data = request.get_json() or {}

    hole_number = data.get("hole_number")
    par = data.get("par")

    if not hole_number or not par:
        return jsonify({"error": "hole_number and par are required"}), 400

    course = GolfCourse.query.get_or_404(course_id)

    hole = Hole(
        course_id=course.id,
        hole_number=hole_number,
        par=par
    )

    db.session.add(hole)
    db.session.commit()

    return jsonify({
        "message": "Hole added successfully",
        "hole_id": hole.id
    }), 201
