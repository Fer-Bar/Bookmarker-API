import os

from flask import Flask, jsonify

from src.database import db
from flask_jwt_extended import JWTManager


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get(
                "SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get(
                "SQLALCHEMY_DATABASE_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get(
                "JWT_SECRET_KEY")
        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)

    JWTManager(app)
    # Blueprint for auth routes in our app
    from src.auth import auth
    app.register_blueprint(auth)
    # Blueprint for non-auth routes of app
    from src.bookmarks import bookmarks
    app.register_blueprint(bookmarks)

    return app

