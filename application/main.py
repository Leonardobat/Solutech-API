# -*- coding: utf-8 -*-
""" This is a simple of web index, all methods are implemented on specific blueprints.
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

bp = Blueprint("web", __name__)


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
        if response.status_code == requests.codes.ok:
            return 200
        else:
            return json.jsonify(error=response.json()), 400

    else:
        return (
            json.jsonify(msg="Read the API documentation for how to use this endpoint"),
            400,
        )