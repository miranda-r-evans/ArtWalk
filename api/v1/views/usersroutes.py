#!/usr/bin/env python3
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import User, WalkingRoute
from mongoengine.errors import OperationError, ValidationError, InvalidQueryError, LookUpError


@app_views.route('/usersroutes/liked/<user_id>', methods=['GET', 'PUT'])
def liked(user_id=None):
    '''

    '''
    if user_id is None:
        abort(404, 'Not Found')

    try:
        user = User.objects.get(id=user_id)
    except (OperationError, ValidationError, InvalidQueryError, LookUpError):
        abort(404, 'Not Found')

    if request.method == 'GET':
        liked_routes = []
        for route_id in user['liked']:
            liked_routes.append(WalkingRoute.objects.get(id=route_id).to_dict())
        return jsonify(liked_routes)

    # if method == put
    req = request.get_json()
    if req is None:
        abort(400, 'Not a JSON')

    if 'route_id' not in req.keys():
        abort(400, 'No route id')

    if req['route_id'] in user['liked']:
        return 'already liked'

    try:
        route = WalkingRoute.objects.get(id=req['route_id'])
    except (OperationError, ValidationError, InvalidQueryError, LookUpError):
        abort(404, 'Not Found')

    user['liked'].append(req['route_id'])
    user.save()
    route['likes'] += 1
    route.save()
    return 'like added'


@app_views.route('/usersroutes/saved/<user_id>', methods=['GET', 'PUT'])
def saved(user_id=None):
    '''

    '''
    if user_id is None:
        abort(404, 'Not Found')

    try:
        user = User.objects.get(id=user_id)
    except (OperationError, ValidationError, InvalidQueryError, LookUpError):
        abort(404, 'Not Found')

    if request.method == 'GET':
        saved_routes = []
        for route_id in user['saved']:
            saved_routes.append(WalkingRoute.objects.get(id=route_id).to_dict())
        return jsonify(saved_routes)

    # if method == put
    req = request.get_json()
    if req is None:
        abort(400, 'Not a JSON')

    if 'route_id' not in req.keys():
        abort(400, 'No route id')

    if req['route_id'] in user['saved']:
        return 'already saved'

    try:
        route = WalkingRoute.objects.get(id=req['route_id'])
    except (OperationError, ValidationError, InvalidQueryError, LookUpError):
        abort(404, 'Not Found')

    user['saved'].append(req['route_id'])
    user.save()
    return 'route saved'


