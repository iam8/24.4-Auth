# Ioana A Mititean
# 24.4 Exercise: Auth
# Flask Feedback

"""
Seed file for Feedback app - clears the database.
"""

from models import db, connect_db
from app import app


if __name__ == "__main__":

    connect_db(app)

    with app.app_context():
        db.drop_all()
        db.create_all()
