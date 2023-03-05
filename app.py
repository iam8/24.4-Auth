# Ioana A Mititean
# 24.4 Exercise: Auth
# Flask Feedback

"""
Flask app for user feedback: route and view definitions.
"""

from flask import Flask, redirect, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, Feedback
from forms import RegisterUserForm, LoginUserForm, AddFeedbackForm, UpdateFeedbackForm


app = Flask(__name__)

app.config["SECRET_KEY"] = "O secreta secreta, of doamne"
debug = DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
# app.config['SQLALCHEMY_ECHO'] = True

# Some common messages to display to user
PLEASE_LOGIN = "NOTICE: You must be logged in to access this page."
PLEASE_LOGOUT = "NOTICE: You must be logged out to access this page."
WRONG_USER_MSG = "NOTICE: You cannot view this page unless you are logged in as that user."
WRONG_CREDS_MSG = "ERROR: Incorrect username and/or password."
UNAME_TAKEN_MSG = "ERROR: That username is unavailable."


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
    redir_profile = check_and_handle_user_logged_in()
    if redir_profile:
        return redir_profile

    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        new_user = User.register(username=username, password=password)
        new_user.email = form.email.data
        new_user.first_name = form.first_name.data
        new_user.last_name = form.last_name.data

        # Display message and redirect to register page if username is taken
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return flash_and_redirect(UNAME_TAKEN_MSG, "/register")

        session["username"] = new_user.username  # Keep user logged in
        return flash_and_redirect(f"Registration successful for user {new_user.username}!",
                                  "/secret")

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
    redir_profile = check_and_handle_user_logged_in()
    if redir_profile:
        return redir_profile

    form = LoginUserForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username  # Keep user logged in
            return flash_and_redirect(f"Welcome back, {user.username}!", f"/users/{user.username}")
        else:
            return flash_and_redirect(WRONG_CREDS_MSG, "/login")

    return render_template("login.jinja2", form=form)


@app.route("/secret")
def display_secret():
    """
    Display a secret message - intended for logged-in users only.
    """

    redir_login = check_and_handle_user_not_logged_in()
    if redir_login:
        return redir_login

    user = db.get_or_404(User, session["username"])
    return render_template("secret.jinja2", user=user)


@app.route("/users/<username>")
def display_user_info(username):
    """
    Display information about the given user, including feedback posted by this user.

    Only logged in users can view this page.
    """

    redir_login = check_and_handle_user_not_logged_in()
    if redir_login:
        return redir_login

    # Users shouldn't be able to access the profile of a different user
    redir_profile = check_and_handle_wrong_user(username)
    if redir_profile:
        return redir_profile

    user = db.get_or_404(User, username)
    feedback = user.feedbacks
    return render_template("user_info.jinja2", user=user, feedback=feedback)


@app.route("/logout")
def logout_user():
    """
    Log user out and redirect to homepage.

    Redirect to login page if user is not currently logged in when accessing this page.
    """

    redir_login = check_and_handle_user_not_logged_in()
    if redir_login:
        return redir_login

    session.pop("username")
    return flash_and_redirect("You have been logged out.", "/")


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """
    Delete the user with the given username, and delete all feedback posted by this user.
        - Only the corresponding logged-in user can delete their profile.

    Log the user out and redirect to homepage.
    """

    redir_login = check_and_handle_user_not_logged_in()
    if redir_login:
        return redir_login

    # Users shouldn't be able to delete the profile of a different user
    redir_profile = check_and_handle_wrong_user(username)
    if redir_profile:
        return redir_profile

    user = db.get_or_404(User, username)
    db.session.delete(user)
    db.session.commit()

    session.pop("username")
    return flash_and_redirect("User successfully deleted.", "/")

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

    redir_login = check_and_handle_user_not_logged_in()
    if redir_login:
        return redir_login

    # Users shouldn't be able to add feedback for a different user
    redir_profile = check_and_handle_wrong_user(username)
    if redir_profile:
        return redir_profile

    user = db.get_or_404(User, username)
    form = AddFeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_fb = Feedback(title=title, content=content, username=username)
        db.session.add(new_fb)
        db.session.commit()

        return flash_and_redirect("Feedback successfully added!", f"/users/{username}")

    return render_template("feedback_add.jinja2", form=form, user=user)


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

    redir_login = check_and_handle_user_not_logged_in()
    if redir_login:
        return redir_login

    feedback = db.get_or_404(Feedback, feedback_id)
    user = feedback.user

    # Users shouldn't be able to add feedback for a different user
    redir_profile = check_and_handle_wrong_user(user.username)
    if redir_profile:
        return redir_profile

    form = UpdateFeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.content = form.content.data
        db.session.commit()

        return flash_and_redirect("Feedback successfully updated!",
                                  f"/users/{session['username']}")

    return render_template("feedback_update.jinja2", form=form, user=user, feedback=feedback)


@app.route("/feedback/<feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """
    Delete the feedback with the given ID.
        - Only the corresponding logged-in user can delete their feedback.

    Redirect to user profile page after feedback is successfully deleted.
    """

    redir_login = check_and_handle_user_not_logged_in()
    if redir_login:
        return redir_login

    feedback = db.get_or_404(Feedback, feedback_id)

    # Users shouldn't be able to delete the feedback written by a different user
    redir_profile = check_and_handle_wrong_user(feedback.user.username)
    if redir_profile:
        return redir_profile

    db.session.delete(feedback)
    db.session.commit()

    return flash_and_redirect("Feedback successfully deleted.", f"/users/{session['username']}")

# -------------------------------------------------------------------------------------------------


# HELPERS -----------------------------------------------------------------------------------------

def flash_and_redirect(msg, redirect_to):
    """
    Flash a given message and return a redirect to a given URL location.
    """

    flash(msg)
    return redirect(redirect_to)


def check_and_handle_user_logged_in():
    """
    Check and handle if user is currently logged in, but must be logged out.

    If the user is logged in:
        - Flash a message and return a redirect to the user's profile page.

    Otherwise, return None.
    """

    if "username" in session:
        return flash_and_redirect(PLEASE_LOGOUT, f"/users/{session['username']}")


def check_and_handle_user_not_logged_in():
    """
    Check and handle if user is currently logged out, but must be logged in.

    If the user is logged out:
        - Flash a message and return a redirect to the login page.

    Otherwise, return None.
    """

    if "username" not in session:
        return flash_and_redirect(PLEASE_LOGIN, "/login")


def check_and_handle_wrong_user(target_uname):
    """
    Check if the given username matches the currently logged-in user.

    If user doesn't match:
        - Flash a message and return a redirect to the current user's profile page.

    Otherwise, return None.
    """

    curr_username = session["username"]
    if curr_username != target_uname:
        return flash_and_redirect(WRONG_USER_MSG, f"/users/{curr_username}")

# -------------------------------------------------------------------------------------------------


if __name__ == "__main__":

    connect_db(app)

    with app.app_context():
        db.create_all()

    app.run(host='127.0.0.1', port=5000, debug=True, threaded=False)
