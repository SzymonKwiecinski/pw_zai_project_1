from flask_wtf import FlaskForm
from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    StringField,
    SubmitField,
    TextAreaField,
    URLField,
    PasswordField,
)
from wtforms.validators import InputRequired, NumberRange, Email, EqualTo, Length

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
