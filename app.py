# Ioana A Mititean
# 24.4 Exercise: Auth
# Flask Feedback

"""
Flask app for user feedback: route and view definitions.
"""

from flask import Flask, redirect, render_template, session, flash
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
def register_user():
    """
    Route & view for registering a new user to the Feedback app:
        - Displays registration form
        - Validates user-entered form values
        - Handles user registration if validation successful
    """

    form = RegisterUserForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        new_user = User.register(username=username, password=password)
        new_user.email = form.email.data
        new_user.first_name = form.first_name.data
        new_user.last_name = form.last_name.data

        db.session.add(new_user)
        db.session.commit()

        session["username"] = new_user.username  # Keep user logged in
        flash(f"Registration successful for user {new_user.username}!")

        return redirect("/secret")

    return render_template("register.jinja2", form=form)


@ app.route("/login", methods=["GET", "POST"])
def login_user():
    """
    Route & view for logging a user in to the Feedback app:
        - Displays login form
        - Validates user-entered form values
        - Handles user authentication
    """

    form = LoginUserForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username  # Keep user logged in
            flash(f"Welcome back, {user.username}!")

            return redirect("/secret")
        else:
            form.username.errors = ["Incorrect username or password"]

            return redirect("/login")

    return render_template("login.jinja2", form=form)


@app.route("/secret")
def display_secret():
    """
    Display a secret message - intended for logged-in users only.
    """

    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/login")

    return render_template("secret.jinja2")


@app.route("/logout")
def logout_user():
    """
    Log user out and redirect to homepage.
    """

    session.pop("username")
    return redirect("/")

# -------------------------------------------------------------------------------------------------


if __name__ == "__main__":

    connect_db(app)

    with app.app_context():
        db.create_all()

    app.run(host='127.0.0.1', port=5000, debug=True, threaded=False)
