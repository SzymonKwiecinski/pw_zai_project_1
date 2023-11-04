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
)
from wtforms.validators import (
    InputRequired,
    NumberRange,
    Email,
    EqualTo,
    Length,
    Regexp,
)
from flask_wtf.file import FileRequired, FileAllowed, FileField

from flask import current_app


class NewCategoryForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    color = ColorField("Color", validators=[InputRequired()])
    icon_svg = FileField(
        "SVG icon",
        validators=[
            FileAllowed(IMAGES, "Only Images"),
            FileRequired("File is required")
        ]
    )
    submit = SubmitField("Save")


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
