#!/usr/bin/env python3
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.walkingroute import WalkingRoute


@app_views.route('/generateRoute', methods=['POST'])
def genR():
    try:
        print('hello')
        req = request.get_json()
        print('data: ', req)
        return jsonify(WalkingRoute.generateRoute(**req))
    except TypeError:
        abort(400, 'Bad Request')
