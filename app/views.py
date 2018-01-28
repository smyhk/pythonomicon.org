from flask import Blueprint
from flask import render_template, redirect, flash, request, url_for, abort
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager
from app.models import db, User, Post
from app.forms import LoginForm, SignupForm, NewPostForm
from urllib.parse import urlparse, urljoin
from datetime import datetime

mod = Blueprint("app", __name__, template_folder="templates", static_folder="static")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@mod.route("/")
def index():
    return render_template("index.html")


@mod.route("/about")
def about():
    return render_template("about.html")


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@mod.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Logged in successfully")

                # TODO: Fix 'next'
                """" 
                dest = request.args.get('next')
                # is_safe_url should check if the url is safe for redirects.
                # See http://flask.pocoo.org/snippets/62/ for an example.
                if not is_safe_url(dest):
                    return abort(400)
                """

                return redirect(url_for('app.index'))

    return render_template("login.html", form=form)


@mod.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="sha256")
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('app.index'))

    return render_template("signup.html", form=form)


@mod.route("/post/<int:post_id>")
def post(post_id):
    blogpost = Post.query.filter_by(id=post_id).one()

    date = blogpost.date_posted.strftime('%B %d, %Y')

    return render_template("post.html", post=blogpost, date_posted=date)


@mod.route("/newpost", methods=["GET", "POST"])
@login_required
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        blogpost = Post(title=form.title.data,
                        subtitle=form.subtitle.data,
                        author_id=current_user.id,
                        content=form.content.data,
                        date_posted=datetime.now())
        db.session.add(blogpost)
        db.session.commit()
        return redirect(url_for('app.index'))

    return render_template("newpost.html", form=form)


@mod.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('app.index'))
