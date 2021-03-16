# -*- coding: utf-8 -*-

import requests
from flask import Blueprint, g, request, json, send_from_directory
from flask_cors import CORS
from application.db.users import Users

bp = Blueprint("web_skill", __name__, url_prefix="/api/skill")
CORS(bp)


@bp.route("/<user>", methods=("GET",))
def index(user) -> tuple:

    url = Users().get_URL(user)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data is not None:
            return json.jsonify(data), 200
    else:
        return 404


@bp.route("/<user>/command/", methods=("POST"))
def commands(user) -> tuple:

    if request.is_json:
        data = request.json
        url = Users().get_URL(user)
        response = requests.post(url, data)
        if response.status_code == 200:
            return 200
        else:
            return json.jsonify(error=response.json()), 400

    else:
        return (
            json.jsonify(msg="Read the API documentation for how to use this endpoint"),
            400,
        )
