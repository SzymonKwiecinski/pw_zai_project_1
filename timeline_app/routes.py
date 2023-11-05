from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    request,
    url_for,
    flash,
)
from icecream import ic
from passlib.hash import pbkdf2_sha256
from sqlalchemy import select, update, delete, func

from timeline_app.database import db
from timeline_app.forms import (
    LoginForm,
    RegisterForm,
    NewCategoryForm,
    EditCategoryForm,
    AddEventForm,
    EditEventForm,
)
from timeline_app.helpers import (
    extract_hash_pwd_with_salt,
    add_config_vars_to_pwd,
    login_required,
    remove_file_from_category,
    remove_file_from_event,
    add_file_to_category,
    add_file_to_event,
    category_exits,
    event_exits,
    SALT_SIZE,
)
from timeline_app.models import User, Category, Event

pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


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
        session["active_event"] = _id
    ic(session.get("active_event"))
    return redirect(url_for(f".index", _anchor=str(_id)))


@pages.route("/delete_event")
def delete_event():
    _id = request.args.get("_id")
    graphic = request.args.get("graphic")
    db.session.execute(delete(Event).where(Event.id == _id))
    if event_exits(graphic):
        remove_file_from_event(graphic)
    db.session.commit()

    return redirect(url_for(".index"))


@pages.route("/edit_event", methods=["GET", "POST"])
def edit_event():
    _id = request.args.get("_id")
    event = db.session.execute(
        select(
            Event.name,
            Event.description,
            Event.start_date,
            Event.graphic,
            Event.end_date,
            Event.category_id,
            Category.name.label("category_name"),
        )
        .join_from(Event, Category)
        .where(Event.id == _id)
    ).one()

    form = EditEventForm()
    categories = db.session.execute(select(Category.name)).all()
    form.category.choices = [c.name for c in categories]

    if form.validate_on_submit():
        if form.start_date.data > form.end_date.data:
            flash("Wrong dates", category="danger")
            return redirect(url_for(".new_event"))

        category = db.session.execute(
            select(Category.id).where(Category.name == form.category.data)
        ).one()

        db.session.execute(
            update(Event)
            .where(Event.id == _id)
            .values(
                name=form.name.data,
                description=form.description.data,
                start_date=form.start_date.data,
                end_date=form.end_date.data,
                category_id=category.id,
            )
        )

        db.session.commit()
        if form.graphic.data and (form.graphic.data.filename != event.graphic):
            db.session.execute(
                update(Event)
                .where(Event.id == _id)
                .values(graphic=form.graphic.data.filename)
            )
            remove_file_from_event(event.graphic)
            add_file_to_event(form.graphic.data)

        db.session.commit()

        return redirect(url_for(".index"))

    form.name.data = event.name
    form.description.data = event.description
    form.start_date.data = event.start_date
    form.end_date.data = event.end_date
    form.category.data = event.category_name

    return render_template("add_event.html", form=form)


@pages.route("/new_event", methods=["GET", "POST"])
def new_event():
    form = AddEventForm()
    categories = db.session.execute(select(Category.name)).all()
    form.category.choices = [c.name for c in categories]

    if form.validate_on_submit():
        if form.start_date.data > form.end_date.data:
            flash("Wrong dates", category="danger")
            return redirect(url_for(".new_event"))

        category = db.session.execute(
            select(Category.id).where(Category.name == form.category.data)
        ).one()

        highest_event = db.session.execute(select(func.max(Event.id))).one()

        event = Event(
            id=highest_event[0] + 1 if highest_event else 1,
            name=form.name.data,
            description=form.description.data,
            graphic=form.graphic.data.filename,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            category_id=category.id,
        )

        db.session.add(event)
        add_file_to_event(form.graphic.data)
        db.session.commit()

        return redirect(url_for(".index"))

    return render_template("add_event.html", form=form)


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

        if category_exits(form.icon_svg.data.filename):
            flash("File with this name exists", category="danger")
            return redirect(url_for(".add_category"))

        highest_category = db.session.execute(select(func.max(Category.id))).one()

        new_category = Category(
            id=highest_category[0] + 1 if highest_category else 1,
            name=form.name.data,
            color=form.color.data,
            icon_svg=form.icon_svg.data.filename,
        )
        db.session.add(new_category)
        db.session.commit()

        add_file_to_category(form.icon_svg.data)

        return redirect(url_for(".edit_categories"))

    return render_template("add_category.html", form=form)


@pages.route("/edit_category/<int:_id>", methods=["GET", "POST"])
def edit_category(_id: int):
    category = db.session.execute(
        select(Category.id, Category.name, Category.color, Category.icon_svg).where(
            Category.id == _id
        )
    ).one()
    form = EditCategoryForm(name=category.name, color=category.color)
    if form.validate_on_submit():
        db.session.execute(
            update(Category)
            .where(Category.id == _id)
            .values(name=form.name.data, color=form.color.data)
        )

        if form.icon_svg.data:
            db.session.execute(
                update(Category)
                .where(Category.id == _id)
                .values(icon_svg=form.icon_svg.data.filename)
            )

            if category_exits(category.icon_svg):
                remove_file_from_category(category.icon_svg)
                add_file_to_category(form.icon_svg.data)

        db.session.commit()
        return redirect(url_for(".edit_categories"))

    return render_template("edit_category.html", form=form, category=category)


@pages.route("/delete_category/<int:_id>", methods=["GET", "POST"])
def delete_category(_id: int):
    icon_svg = request.args.get("icon_svg", None)

    results = db.session.execute(
        select(Event).where(Event.category_id == _id)
    ).fetchall()

    if len(results):
        flash("This category has exists events!!", category="danger")
        return redirect(url_for("pages.edit_category", _id=_id, icon_svg=icon_svg))

    db.session.execute(delete(Category).where(Category.id == _id))
    if category_exits(icon_svg):
        remove_file_from_category(icon_svg)

    db.session.commit()
    return redirect(url_for(".edit_categories"))


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

        highest_user = db.session.execute(select(func.max(Category.id))).one()

        user = User(id=highest_user[0] + 1 if highest_user else 1, email=form.email.data, password=hashed_password_with_salt)
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
