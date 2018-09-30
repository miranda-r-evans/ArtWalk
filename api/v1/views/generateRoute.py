#!/usr/bin/env python3
'''
    routes for generating new map data
'''

from api.v1.views import app_views
from flask import jsonify, request, abort
from models.walkingroute import WalkingRoute


@app_views.route('/generateRoute', methods=['POST'])
def genR():
    '''
        generate map data randomly
    '''
    try:
        req = request.get_json()
        return jsonify(WalkingRoute.generateRoute(**req))
    except TypeError:
        abort(400, 'Bad Request')


@app_views.route('/customRoute', methods=['POST'])
def customR():
    '''
        create map data solely from user input
    '''
    try:
        req = request.get_json()
        return jsonify(WalkingRoute.customRoute(**req))
    except TypeError:
        abort(400, 'Bad Request')
