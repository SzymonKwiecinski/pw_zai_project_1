from datetime import datetime

from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    StringField,
    SubmitField,
    TextAreaField,
    URLField,
    PasswordField,
    SelectField,
    ColorField,
    DateField,
)
from wtforms.validators import (
    InputRequired,
    NumberRange,
    Email,
    EqualTo,
    Length,
    Regexp,
    DataRequired,

)
from flask_wtf.file import FileRequired, FileAllowed, FileField

from flask import current_app


class EventForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[InputRequired()])
    graphic = FileField(
        "Graphic PNG",
        validators=[
            FileAllowed(["png"], "Only PNG format"),
            FileRequired("File is required"),
        ],
    )
    start_date = DateField("Start date", default=datetime.now(), validators=[InputRequired(), DataRequired()])
    end_date = DateField("End date", default=datetime.now(), validators=[InputRequired(), DataRequired()])
    category = SelectField("Category", choices=[])



class AddEventForm(EventForm):
    submit = SubmitField("Add new")


class EditEventForm(EventForm):
    submit = SubmitField("Save Edited")


class CategoryForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    color = ColorField("Color", validators=[InputRequired()])
    icon_svg = FileField(
        "SVG icon",
        validators=[
            FileAllowed(["svg"], "Only Images"),
            FileRequired("File is required"),
        ],
    )


class NewCategoryForm(CategoryForm):
    submit = SubmitField("Save New")


class EditCategoryForm(CategoryForm):
    icon_svg = FileField(
        "New SVG Icon",
    )
    submit = SubmitField("Save Edited")


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])

    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            Length(
                min=1,
                max=20,
                message="Your password must be between 4 and 20 characters long.",
            ),
        ],
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            InputRequired(),
            EqualTo(
                "password",
                message="This password did not match the one in the password field.",
            ),
        ],
    )

    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")
