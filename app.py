# Ioana A Mititean
# 24.4 Exercise: Auth
# Flask Feedback

"""
Flask app for user feedback: route and view definitions.
"""

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db


app = Flask(__name__)

app.config["SECRET_KEY"] = "O secreta secreta, of doamne"
debug = DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
# app.config['SQLALCHEMY_ECHO'] = True


if __name__ == "__main__":

    connect_db(app)

    with app.app_context():
        db.create_all()

    app.run(host='127.0.0.1', port=5000, debug=True, threaded=False)
