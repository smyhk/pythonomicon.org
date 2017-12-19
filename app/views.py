from flask import Blueprint
from flask import render_template, redirect, flash, request, url_for, abort
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager
from app.models import db
from app.forms import LoginForm, SignupForm
from urllib.parse import urlparse, urljoin

mod = Blueprint("app", __name__, template_folder="templates", static_folder="static")


@login_manager.user_loader
def load_user(user_id):
    return db.User.query.get(int(user_id))


@mod.route("/")
def index():
    return render_template("index.html")


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@mod.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = db.User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Logged in successfully")

                dest = request.args.get('next')
                # is_safe_url should check if the url is safe for redirects.
                # See http://flask.pocoo.org/snippets/62/ for an example.
                if not is_safe_url(dest):
                    return abort(400)

                return redirect(next or url_for('app.index'))

    return render_template("login.html", form=form)


@mod.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="sha256")
        new_user = db.User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('app.index'))

    return render_template("signup.html", form=form)


@mod.route("/home")
@login_required
def home():
    return "I should not see this unless logged in"


@mod.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('app.index'))
