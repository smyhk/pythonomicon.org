from flask import Blueprint
from flask import render_template

mod = Blueprint("app", __name__, template_folder="templates", static_folder="static")


@mod.route("/")
def index():
    return render_template("index.html")


@mod.route("/login")
def login():
    return render_template("login.html")


@mod.route("/signup")
def signup():
    return render_template("signup.html")
