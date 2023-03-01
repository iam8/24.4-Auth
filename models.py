# Ioana A Mititean
# 24.4 Exercise: Auth
# Flask Feedback

"""
Models for feedback app.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """
    Connect Flask app to SQLA database.
    """

    db.app = app
    db.init_app(app)


class User(db.Model):
    """
    Model for a user.
    """

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(cls, username, password):
        """
        Register user with hashed password and return the user.
        """

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        # Return instance of user with username and hashed password
        return cls(username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, password):
        """
        Validate that the user exists and the password is correct.

        Return the user object if valid; otherwise return False.
        """

        # Return single matching User object or None
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False
