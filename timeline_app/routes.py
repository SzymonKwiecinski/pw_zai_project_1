from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    request,
    current_app,
    url_for,
    abort,
    flash
)
from timeline_app.forms import LoginForm, RegisterForm

pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)

@pages.route("/")
def index():
    return render_template("index.html")



@pages.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()
    print(form.hidden_tag())
    


    return render_template("login.html", form=form)


@pages.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")
