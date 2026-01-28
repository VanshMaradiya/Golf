from flask import Blueprint, request, jsonify
from services.score_service import add_or_update_score, get_user_scores

score_bp = Blueprint("score", __name__, url_prefix="/api/scores")


# ---------------------------
# ADD / UPDATE SCORE
# ---------------------------
@score_bp.route(
    "/tournaments/<int:tournament_id>/holes/<int:hole_id>",
    methods=["POST"]
)
def add_score(tournament_id, hole_id):
    user_id = request.headers.get("X-User-Id")

    if not user_id:
        return jsonify({"error": "X-User-Id header required"}), 401

    data = request.get_json(silent=True) or {}
    strokes = data.get("strokes")

    success, message = add_or_update_score(
        user_id=int(user_id),
        tournament_id=tournament_id,
        hole_id=hole_id,
        strokes=strokes
    )

    if not success:
        return jsonify({"error": message}), 400

    return jsonify({"message": message}), 200


# ---------------------------
# GET MY SCORES
# ---------------------------
@score_bp.route("/tournaments/<int:tournament_id>/my-scores", methods=["GET"])
def my_scores(tournament_id):
    user_id = request.headers.get("X-User-Id")

    if not user_id:
        return jsonify({"error": "X-User-Id header required"}), 401

    success, data = get_user_scores(int(user_id), tournament_id)

    if not success:
        return jsonify({"error": data}), 400

    return jsonify(data), 200
