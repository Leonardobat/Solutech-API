# -*- coding: utf-8 -*-
""" This is the API interface, create to be a proxy for external requests and the internal ones
"""
from pathlib import Path
from flask import (
    Blueprint,
    flash,
    g,
    render_template,
    redirect,
    url_for,
    request,
    json,
)
import requests
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.db.users import Users
from flask_cors import CORS

bp = Blueprint("web", __name__)
CORS(bp)


@bp.route("/<user>/info", methods=("GET",))
@jwt_required
def index(user) -> tuple:
    if user == get_jwt_identity():
        return json.jsonify(user=user), 200
    else:
        return 404


@bp.route("/<user>/info", methods=("PUT",))
@jwt_required
def update_user(user) -> tuple:

    if user == get_jwt_identity():
        return 200
    else:
        return 404


@bp.route("/<user>/command/", methods=("GET", "POST"))
def commands(user) -> tuple:

    if request.method == "POST" and request.is_json:
        data = request.json
        url = Users().get_URL(user)
        response = requests.post(url, data)
        if response.status_code != 200:
            return json.jsonify(error=response.json()), 400
        else:
            return 200

    else:
        return (
            json.jsonify(msg="Read the API documentation for how to use this endpoint"),
            400,
        )