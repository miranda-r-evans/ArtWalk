#!/usr/bin/env python3
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
from mongoengine.errors import OperationError, ValidationError, InvalidQueryError, LookUpError


@app_views.route('/users', methods=['GET', 'POST'])
def show_all_or_create_user():
    '''
        shows all users or creates a new user
    '''
    if request.method == 'GET':
        users = [item.to_dict() for item in User.objects()]
        return jsonify(users)

    # if method == post
    req = request.get_json()
    new = User(**req)
    new.save()
    return new.__str__()


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def user_by_id(user_id=None):
    '''
        shows, deletes, or updates one user
    '''
    if user_id is None:
        abort(404, 'Not Found')

    try:
        user = User.objects(id=user_id)[0]
    except IndexError:
        abort(404, 'Not Found')

    if request.method == 'GET':
        return user.__str__()

    if request.method == 'DELETE':
        user.delete()
        return jsonify({}), 200

    # if method == put
    req = request.get_json()
    if req is None:
        abort(400, 'Not a JSON')
    try:
        user.update(**req)
        user = User.objects(id=user_id)[0]
        return user.__str__()
    except (OperationError, ValidationError, InvalidQueryError, LookUpError):
        abort(400, 'Bad Data')
