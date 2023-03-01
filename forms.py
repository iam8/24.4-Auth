# Ioana A Mititean
# 24.4 Exercise: Auth
# Flask Feedback

"""
Form model creation and setup.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Email


class RegisterUserForm(FlaskForm):
    """
    Model for the form a user will fill out to register for the Feedback app.
    """

    username = StringField("Username",
                           validators=[InputRequired()],
                           render_kw={"placeholder": "Enter a username"})

    password = PasswordField("Password",
                             validators=[InputRequired()],
                             render_kw={"placeholder": "Enter a password"})

    email = EmailField("Email",
                       validators=[InputRequired(), Email()],
                       render_kw={"placeholder": "Enter your email address"})

    first_name = StringField("First name",
                             validators=[InputRequired()],
                             render_kw={"placeholder": "Enter your first name"})

    last_name = StringField("last name",
                            validators=[InputRequired()],
                            render_kw={"placeholder": "Enter your last name"})


class LoginUserForm(FlaskForm):
    """
    Model for the form a user will fill out to login to the Feedback app.
    """

    username = StringField("Username",
                           validators=[InputRequired()],
                           render_kw={"placeholder": "Enter your username"})

    password = PasswordField("Password",
                             validators=[InputRequired()],
                             render_kw={"placeholder": "Enter your password"})
