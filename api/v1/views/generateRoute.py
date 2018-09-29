#!/usr/bin/env python3
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.walkingroute import WalkingRoute


@app_views.route('/generateRoute', methods=['POST'])
def genR():
    try:
        req = request.get_json()
        return jsonify(WalkingRoute.generateRoute(**req))
    except TypeError:
        abort(400, 'Bad Request')


@app_views.route('/customRoute', methods=['POST'])
def customR():
    try:
        req = request.get_json()
        return jsonify(WalkingRoute.customRoute(**req))
    except TypeError:
        abort(400, 'Bad Request')
