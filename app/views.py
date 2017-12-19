from flask import Blueprint
from flask import render_template, redirect, flash, request
from flask_login import login_user, login_required, logout_user
from app import login_manager
from app.models import User

mod = Blueprint("app", __name__, template_folder="templates", static_folder="static")


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@mod.route("/")
def index():
    return render_template("index.html")


@mod.route("/signup")
def signup():
    return render_template("signup.html")


@mod.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@mod.route("/userlogin", methods=["GET", "POST"])
def user_login():
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username, password=password).first()
    if not user or not password:
        flash("Check username or password.")

    login_user(user)

    flash("You are now logged in.")
    return redirect("index.html")


@mod.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect("index.html")
