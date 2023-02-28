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
