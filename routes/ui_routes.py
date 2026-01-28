from flask import Blueprint, render_template

ui_bp = Blueprint("ui", __name__)

@ui_bp.route("/")
def login_page():
    return render_template("login.html")

@ui_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@ui_bp.route("/admin")
def admin_page():
    return render_template("admin.html")

@ui_bp.route("/player")
def player_page():
    return render_template("player.html")

@ui_bp.route("/leaderboard")
def leaderboard_page():
    return render_template("leaderboard.html")

@ui_bp.route("/register")
def register_page():
    return render_template("register.html")

