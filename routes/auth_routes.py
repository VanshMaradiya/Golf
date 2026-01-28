from flask import Blueprint, request, jsonify
from extensions import db
from models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


# ---------------------------
# REGISTER
# ---------------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "player")

    if not name or not email or not password:
        return jsonify({"error": "Name, email and password are required"}), 400

    if role not in ("admin", "player"):
        return jsonify({"error": "Invalid role"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    user = User(name=name, email=email, role=role)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully",
        "user_id": user.id,
        "role": user.role
    }), 201


# ---------------------------
# LOGIN (NO COOKIE)
# ---------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    # 🔹 Just return user_id
    return jsonify({
        "message": "Login successful",
        "user_id": user.id,
        "role": user.role
    }), 200


# ---------------------------
# LOGOUT (STATELESS)
# ---------------------------
@auth_bp.route("/logout", methods=["POST"])
def logout():
    return jsonify({
        "message": "Logout successful. Please clear user data on client."
    }), 200
