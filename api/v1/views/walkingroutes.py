#!/usr/bin/env python3
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.walkingroute import WalkingRoute
from mongoengine.errors import OperationError, ValidationError, InvalidQueryError, LookUpError


@app_views.route('/walkingroutes', methods=['GET', 'POST'])
def show_all_or_create_route():
    '''
        shows all users or creates a new route
    '''
    if request.method == 'GET':
        routes = [item.to_dict() for item in WalkingRoute.objects()]
        return jsonify(routes)

    # if method == post
    req = request.get_json()
    new = WalkingRoute(**req)
    new.save()
    return new.__str__()


@app_views.route('/walkingroutes/<route_id>', methods=['GET', 'DELETE', 'PUT'])
def route_by_id(route_id=None):
    '''
        shows, deletes, or updates one route
    '''
    if route_id is None:
        abort(404, 'Not Found')

    try:
        route = WalkingRoute.objects(id=route_id)[0]
    except IndexError:
        abort(404, 'Not Found')

    if request.method == 'GET':
        return route.__str__()

    if request.method == 'DELETE':
        route.delete()
        return jsonify({})

    # if method == put
    req = request.get_json()
    if req is None:
        abort(400, 'Not a JSON')
    try:
        route.update(**req)
        route = WalkingRoute.objects(id=route_id)[0]
        return route.__str__()
    except (OperationError, ValidationError, InvalidQueryError, LookUpError):
        abort(400, 'Bad Data')
