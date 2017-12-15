from flask import Blueprint
from flask import render_template

mod = Blueprint("app", __name__, template_folder="templates")


@mod.route("/")
def index():
    return render_template("index.html")
