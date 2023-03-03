# Ioana A Mititean
# 24.4 Exercise: Auth
# Flask Feedback

"""
Seed file for Feedback app - clears the database.
"""

from models import db, connect_db, User, Feedback
from app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


if __name__ == "__main__":

    connect_db(app)

    with app.app_context():
        db.drop_all()
        db.create_all()

        pw1 = bcrypt.generate_password_hash("dragon1").decode("utf8")
        pw2 = bcrypt.generate_password_hash("dragon2").decode("utf8")

        a1 = User(username="a1",
                  password=pw1,
                  email="a1@a1.com",
                  first_name="a1",
                  last_name="mit1")

        a2 = User(username="a2",
                  password=pw2,
                  email="a2@a2.com",
                  first_name="a2",
                  last_name="mit2")

        db.session.add_all([a1, a2])
        db.session.commit()

        fb1 = Feedback(title="FB1 by a1",
                       content="Example feedback 1",
                       username="a1")

        fb2 = Feedback(title="FB2 by a2",
                       content="Example feedback 2",
                       username="a2")

        fb3 = Feedback(title="FB3 by a2",
                       content="Example feedback 3",
                       username="a2")

        db.session.add_all([fb1, fb2, fb3])
        db.session.commit()
