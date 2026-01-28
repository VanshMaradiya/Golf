from functools import wraps
from flask import request, jsonify


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = request.headers.get("X-User-Id")
        role = request.headers.get("X-User-Role")

        if not user_id:
            return jsonify({"error": "Authentication required"}), 401

        if role != "admin":
            return jsonify({"error": "Admin access required"}), 403

        return fn(*args, **kwargs)
    return wrapper


def player_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = request.headers.get("X-User-Id")
        role = request.headers.get("X-User-Role")

        if not user_id:
            return jsonify({"error": "Authentication required"}), 401

        if role != "player":
            return jsonify({"error": "Player access required"}), 403

        return fn(*args, **kwargs)
    return wrapper
