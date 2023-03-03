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

PLEASE_LOGIN = "NOTICE: You must be logged in to access this page."
PLEASE_LOGOUT = "NOTICE: You must be logged out to access this page."

# TODO: handle case when a user tries to enter an existing username in registration - currently,
# the app will just crash


# USER ROUTES -------------------------------------------------------------------------------------

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

    Flash a message and redirect to user info page if user is not currently logged out when trying
    to access this page.
    """

    # Handle case when user is already logged in
    if "username" in session:
        flash(PLEASE_LOGOUT)
        return redirect(f"/users/{session['username']}")

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

    Flash a message and redirect to user info page if user is not currently logged out when trying
    to access this page.
    """

    # Handle case when user is already logged in
    if "username" in session:
        flash(PLEASE_LOGOUT)
        return redirect(f"/users/{session['username']}")

    form = LoginUserForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username  # Keep user logged in
            flash(f"Welcome back, {user.username}!")

            return redirect(f"/users/{user.username}")
        else:
            flash("ERROR: incorrect username and/or password")
            return redirect("/login")

    return render_template("login.jinja2", form=form)


@app.route("/secret")
def display_secret():
    """
    Display a secret message - intended for logged-in users only.
    """

    if "username" not in session:
        flash(PLEASE_LOGIN)
        return redirect("/login")

    user = db.get_or_404(User, session["username"])
    return render_template("secret.jinja2", user=user)


@app.route("/users/<username>")
def display_user_info(username):
    """
    Display information about the given user, including feedback posted by this user.

    Only logged in users can view this page.
    """

    if "username" not in session:
        flash(PLEASE_LOGIN)
        return redirect("/login")

    # User's shouldn't be able to access the profile of a different user
    curr_username = session["username"]
    if curr_username != username:
        flash("You cannot view this page unless you are logged in as that user!")
        return redirect(f"/users/{curr_username}")

    user = db.get_or_404(User, username)
    feedback = user.feedbacks
    return render_template("user_info.jinja2", user=user, feedback=feedback)


@app.route("/logout")
def logout_user():
    """
    Log user out and redirect to homepage.

    Redirect to homepage if user is not currently logged in when accessing this page.
    """

    if "username" not in session:
        flash(PLEASE_LOGIN)
        return redirect("/login")

    session.pop("username")
    flash("You have been logged out.")
    return redirect("/")


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """
    Delete the user with the given username, and delete all feedback posted by this user.
        - Only the corresponding logged-in user can delete their profile.

    Log the user out and redirect to homepage.

    """

# -------------------------------------------------------------------------------------------------


# Feedback routes ---------------------------------------------------------------------------------

@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """
    Route & view for adding feedback for the given user:
        - Display feedback form
        - Validate user-entered form values
        - Add the new feedback to this user

    Only the corresponding logged-in user can add feedback.

    Redirect to user profile page after feedback is successfully added.
    """


@app.route("/feedback/<feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """
    Route & view for updating feedback for the given user:
        - Display feedback edit form
        - Validate user-entered form values
        - Update the new feedback for this user

    Only the corresponding logged-in user can update their feedback.

    Redirect to user profile page after feedback is successfully updated.
    """


@app.route("/feedback/<feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """
    Delete the feedback with the given ID.
        - Only the corresponding logged-in user can delete their feedback.

    Redirect to user profile page after feedback is successfully deleted.
    """


# -------------------------------------------------------------------------------------------------


if __name__ == "__main__":

    connect_db(app)

    with app.app_context():
        db.create_all()

    app.run(host='127.0.0.1', port=5000, debug=True, threaded=False)
