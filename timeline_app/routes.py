import functools

from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    request,
    current_app,
    url_for,
    abort,
    flash,
)
from passlib.hash import pbkdf2_sha256
from timeline_app.database import db
from timeline_app.forms import LoginForm, RegisterForm
from timeline_app.models import User
from sqlalchemy import select

HASH_TYPE = "pbkdf2-sha256"
ROUND = "29000"
SALT_SIZE = 32


def extract_hash_pwd_with_salt(pbkdf2_sha256_output: str) -> str:
    return pbkdf2_sha256_output.split("$", maxsplit=3)[-1]


def add_config_vars_to_pwd(hash_pwd_with_salt: str) -> str:
    return f"${HASH_TYPE}${ROUND}${hash_pwd_with_salt}"


pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


def login_required(route):
    @functools.wraps(route)
    def route_wrapper(*args, **kwargs):
        if session.get("email") is None:
            return redirect(url_for(".login"))

        return route(*args, **kwargs)

    return route_wrapper


@pages.route("/")
@login_required
def index():
    return render_template("index.html")


@pages.route("/login", methods=["GET", "POST"])
def login():
    if session.get("email"):
        return redirect(url_for(".index"))

    form = LoginForm()
    if form.validate_on_submit():
        results = db.session.execute(
            select(User.id, User.email, User.password).where(
                User.email == form.email.data
            )
        ).fetchone()

        if not results:
            flash("Login credentials not correct", category="danger")
            return redirect(url_for(".login"))

        pwd = add_config_vars_to_pwd(results.password)
        if pbkdf2_sha256.verify(form.password.data, pwd):
            session["user_id"] = results.id
            session["email"] = results.email

            flash("User logged in successfully", "success")

            return redirect(url_for(".index"))

        flash("Login credentials not correct", category="danger")

    return render_template("login.html", form=form)


@pages.route("/register", methods=["GET", "POST"])
def register():
    if session.get("email"):
        return redirect(url_for(".login"))

    form = RegisterForm()

    if form.validate_on_submit():
        results = db.session.execute(
            select(User.email).where(User.email == form.email.data)
        ).fetchall()


        if results:
            flash("This Email exist", "danger")
            return redirect(url_for(".register"))

        pbkdf2_sha256_password = pbkdf2_sha256.hash(
            form.password.data, salt_size=SALT_SIZE
        )
        hashed_password_with_salt = extract_hash_pwd_with_salt(pbkdf2_sha256_password)
        user = User(email=form.email.data, password=hashed_password_with_salt)
        db.session.add(user)
        db.session.commit()

        flash("User registered successfully", "success")

        return redirect(url_for(".index"))

    return render_template("register.html", form=form)


@pages.route("/logout")
def logout():
    current_theme = session.get("theme")
    session.clear()
    session["theme"] = current_theme

    return redirect(url_for(".login"))


@pages.get("/toggle-theme")
def toggle_theme():
    current_theme = session.get("theme")
    if current_theme == "dark":
        session["theme"] = "light"
    else:
        session["theme"] = "dark"

    return redirect(request.args.get("current_page"))
