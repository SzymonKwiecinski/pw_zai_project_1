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
from timeline_app.database import db
from timeline_app.forms import LoginForm, RegisterForm
from timeline_app.models import User

pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


@pages.route("/")
def index():
    return render_template("index.html")


@pages.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        pass

    return render_template("login.html", form=form)


@pages.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            **{
                "id": 1,
                "nick": form.nick.data,
                "email": form.email.data,
                "password": form.password.data,
            }
        )
        db.session.add(user)
        db.session.commit()

    return render_template("register.html", form=form)
