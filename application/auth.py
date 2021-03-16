# -*- coding: utf-8 -*-
""" Auth Blueprint
    This blueprint manages authentications from clients.
    :Authors: Leonardo B.
"""
from flask import (
    Blueprint,
    g,
    redirect,
    json,
    request,
    url_for,
    wrappers,
)
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import cross_origin
from application.db.users import Users

bp = Blueprint("auth", __name__, url_prefix="/")


@bp.route("/api/login", methods=("GET", "POST"))
@cross_origin()
def login_API() -> tuple:
    """This function registers a new user's session on the server.

    This function expects a JSON with the username and password if
    the user login is successful then it will return the access token.

    Notes
    -----
    The expected JSON has this format {"user":"`USERNAME`" ;"passw":"`PASSWORD`"}
    The return JSON has this format {"access_token":"`TOKEN`"}

    """
    if request.method == "POST" and request.is_json:
        data = request.json
        error = None

        if not data["user"]:
            error = "Missing username parameter"
        if not data["passw"]:
            error = "Missing password parameter"

        user = Users().get_login(user)

        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user["password"], data["passw"]):
            error = "Incorrect password"

        if error is None:
            access_token = create_access_token(identity=data["user"])
            return json.jsonify(access_token=access_token), 200
        else:
            return json.jsonify(error=error), 401

    return json.jsonify(error="Missing JSON in request"), 400
