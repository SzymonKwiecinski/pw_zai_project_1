import functools
import os

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
from werkzeug.utils import secure_filename

from timeline_app.database import db
from timeline_app.forms import LoginForm, RegisterForm, NewCategoryForm
from timeline_app.models import User, Category, Event
from sqlalchemy import select, alias
from icecream import ic

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
    categories = db.session.execute(
        select(Category.id, Category.name, Category.color, Category.icon_svg)
    ).all()
    if session.get("active_categories") is None:
        session["active_categories"] = [category.id for category in categories]

    events = db.session.execute(
        select(
            Event.id,
            Event.name,
            Event.description,
            Event.graphic,
            Event.start_date,
            Event.end_date,
            Category.id.label("category_id"),
            Category.name.label("category_name"),
            Category.color.label("category_color"),
        )
        .join_from(Event, Category)
        .order_by(Event.start_date.desc())
    ).fetchall()

    return render_template("index.html", categories=categories, events=events)

@pages.route("/event/<int:_id>")
def event(_id: int):
    active_event = session.get("active_event")

    if active_event and _id == active_event:
        session.pop("active_event")
    else:
        session['active_event'] = _id
    ic(session.get('active_event'))
    return redirect(url_for(f".index", _anchor=str(_id)))

@pages.route("/category/<int:_id>")
def category(_id: int):
    active_categories: list = session.get("active_categories")

    if _id in active_categories:
        active_categories.remove(_id)
    else:
        active_categories.append(_id)

    session["active_categories"] = active_categories
    return redirect(url_for(".index"))


@pages.route("/edit_categories")
def edit_categories():
    categories = db.session.execute(
        select(Category.id, Category.name, Category.color, Category.icon_svg)
    ).all()

    return render_template("edit_categories.html", categories=categories)


@pages.route("/add_category", methods=["GET", "POST"])
def add_category():
    form = NewCategoryForm()
    if form.validate_on_submit():
        ic(f"timeline_app/static/img/category/{form.icon_svg.data.filename}")
        if os.path.isfile(f"timeline_app/static/img/category/{form.icon_svg.data.filename}"):
            flash("File with this name exists", category="danger")
            return redirect(url_for(".add_category"))


        new_category = Category(name=form.name.data, color=form.color.data, icon_svg=form.icon_svg.data.filename)
        db.session.add(new_category)
        db.session.commit()
        current_app.photos.save(form.icon_svg.data, folder="category")


        return redirect(url_for(".edit_categories"))

    return render_template("add_category.html", form=form)




@pages.route("/edit_category/<int:_id>")
def edit_category(_id: int):
    category = db.session.execute(
        select(Category.id, Category.name, Category.color, Category.icon_svg).where(Category.id == _id)
    ).one()



    return render_template("edit_categories.html", categories=categories, edit_category=category)


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
