"""
Main flask server functionality and logic.
"""
# pylint: disable=no-member
# pylint: disable=wrong-import-position
# pylint: disable=global-statement
import os
import logging
from os.path import join, dirname
from dotenv import load_dotenv
import flask
import flask_socketio
import flask_sqlalchemy
from google.oauth2 import id_token
from google.auth.transport import requests
from datetime import datetime

logging.getLogger("werkzeug").setLevel(logging.ERROR)

app = flask.Flask(__name__)

##BOILER PLATE CODE TO INITIATE SOCKETS
socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), "sql.env")
load_dotenv(dotenv_path)

# BOILER PLATE CODE TO INSTANTIATE PSQL AND SQLALCHEMY

database_uri = os.environ["DATABASE_URL"]

app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)

db.init_app(app)
db.app = app


CALENDER_EVENT_CHANNEL = "calendar_event"

import models


def push_new_user_to_db(ident, name, email):
    """
    Pushes new user to database.
    """
    db.session.add(models.AuthUser(ident, name, email))
    db.session.commit()


def get_sid():
    """
    returns sid.
    """
    sid = flask.request.sid
    return sid


##SOCKET EVENTS
@socketio.on("connect")
def on_connect():
    """
    Runs on connect.
    """
    print("Someone connected!")


@socketio.on("disconnect")
def on_disconnect():
    """
    Runs on disconnect.
    """
    print("Someone disconnected!")


@socketio.on("new google user")
def on_new_google_user(data):
    """
    Runs verification on google token.
    """
    print("Beginning to authenticate data: ", data)
    sid = get_sid()
    try:
        idinfo = id_token.verify_oauth2_token(
            data["idtoken"],
            requests.Request(),
            "658056760445-ejq8q635n1948vqieqf95vsa6c6e1fvp.apps.googleusercontent.com",
        )
        userid = idinfo["sub"]
        print("Verified user. Proceeding to check database.")
        exists = (
            db.session.query(models.AuthUser.userid).filter_by(userid=userid).scalar()
            is not None
        )
        if not exists:
            push_new_user_to_db(userid, data["name"], data["email"])
        all_ccodes = [
            record.ccode
            for record in db.session.query(models.Calendars)
            .filter_by(userid=userid)
            .all()
        ]
        socketio.emit(
            "Verified", {"name": data["name"], "ccodes": all_ccodes}, room=sid
        )
        return userid
    except ValueError:
        # Invalid token
        print("Could not verify token.")
        return "Unverified."
    except KeyError:
        print("Malformed token.")
        return "Unverified."



@app.route("/")
def hello():
    """
    Runs at page-load.
    """
    models.db.create_all()
    db.session.commit()
    return flask.render_template("index.html")


if __name__ == "__main__":
    socketio.run(
        app,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),
        debug=True,
    )