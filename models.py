# Ioana A Mititean
# 24.4 Exercise: Auth
# Flask Feedback

"""
Models for feedback app.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
