# Ioana A Mititean
# 24.4 Exercise: Auth
# Flask Feedback

"""
Flask app for user feedback: route and view definitions.
"""

from flask import Flask, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User
from forms import RegisterUserForm, LoginUserForm


app = Flask(__name__)

app.config["SECRET_KEY"] = "O secreta secreta, of doamne"
debug = DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
# app.config['SQLALCHEMY_ECHO'] = True


# ROUTES & VIEWS ----------------------------------------------------------------------------------

@app.route("/")
def display_home():
    """
    Homepage route.
    """

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def display_register_form():
    """
    Display a form for a user to register with.

    Route & view for registering a new user to the Feedback app.
        - Displays registration form
        - Validates user-entered form values
        - Handles user registration if validation successful
    """

    form = RegisterUserForm()

    if form.validate_on_submit():

        new_user = User()
        form.populate_obj(new_user)

        db.session.add(new_user)
        db.session.commit()

        flash(f"Registration successful for user {new_user.username}!")
        return redirect("/secret")

    return render_template("register.jinja2", form=form)


@app.route("/login")
def display_login_form():
    """
    Display a form for a user to login with.
    """


@app.route("/login", methods=["POST"])
def login_user():
    """
    Handle user login.
    """


@app.route("/secret")
def display_secret():
    """
    Display a secret message.
    """

    return "You made it!"

# -------------------------------------------------------------------------------------------------


if __name__ == "__main__":

    connect_db(app)

    with app.app_context():
        db.create_all()

    app.run(host='127.0.0.1', port=5000, debug=True, threaded=False)
