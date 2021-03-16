from os import urandom
from pathlib import Path
from flask_jwt_extended import JWTManager
from flask import Flask

jwt = JWTManager()


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=urandom(16),
        JWT_SECRET_KEY=urandom(16),
        JWT_ERROR_MESSAGE_KEY="error",
        MAX_CONTENT_LENGTH=1 * 1024 * 1024,
    )

    if config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(config)

    jwt.init_app(app)

    from . import auth, main, skill

    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(skill.bp)
    app.add_url_rule("/api/", endpoint="index")

    return app