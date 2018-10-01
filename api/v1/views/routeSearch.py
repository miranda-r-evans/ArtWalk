#!/usr/bin/env python3
'''
    routes for displaying a tailored list of routes
'''

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import WalkingRoute
from mongoengine.errors import OperationError, ValidationError, InvalidQueryError, LookUpError


@app_views.route('/routeSearch/<keyword>')
def routeSearch(keyword):
    '''
        route to search based on a key word
    '''
    keyword = keyword.replace('%20', ' ')
    routes = list(set(WalkingRoute.objects(name=keyword))|set(WalkingRoute.objects(keywords=keyword)))
    routes.sort(key = lambda x:x['likes'], reverse=True)
    return jsonify([route.to_dict() for route in routes])


@app_views.route('/top10')
def top10():
    '''
        return 10 most popular results
    '''
    return jsonify([route.to_dict() for route in WalkingRoute.objects.order_by('-likes')[:10]])
