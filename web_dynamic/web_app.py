#!/usr/bin/env python3

import requests
from flask import Flask, render_template, url_for, redirect, flash, session, request, abort
from uuid import uuid4
from os import getenv, urandom
from flask_login import LoginManager, current_user, login_user
from models import User
from GoogleAPIKey import APIKey
from flask_cors import CORS, cross_origin


application = Flask(__name__)
application.url_map.strict_slashes = False
port = int(getenv('HBNB_API_PORT', '5001'))
host = '0.0.0.0'
login = LoginManager(application)
cors = CORS(application)


@application.route('/')
def home(route=None):
    '''
        main page of app without login
    '''
    return render_template('index.html', APIKey=APIKey, route=route)


@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return home()

    try:
        req = request.form.to_dict()
        user = User.objects.get(email=req['email'])
    except StopIteration:
        abort(400)

    if req['password'] == user.password:
        session['logged_in'] = True
        session['userId'] = str(user.id)
    else:
        flash('wrong password!')
    return home()


@application.route("/logout")
def logout():
    session['logged_in'] = False
    session.pop('userId')
    return home()


@application.route("/save", methods=['POST'])
def like():
    req = request.form.to_dict()
    try:
        userId = session['userId']
    except KeyError:
        abort(404)

    req['keywords'] = req['keywords'].split(',')
    req['waypoints'] = req['waypoints'].split(',')
    req['likes'] = 1

    route = requests.post('http://127.0.0.1:5000/api/v1/walkingroutes', json=req, headers={'Content-Type': 'application/json'})
    requests.put('http://127.0.0.1:5000/api/v1/usersroutes/saved/' + userId, json={'route_id': route.json()['id']}, headers={'Content-Type': 'application/json'})
    requests.put('http://127.0.0.1:5000/api/v1/usersroutes/liked/' + userId, json={'route_id': route.json()['id']}, headers={'Content-Type': 'application/json'})

    return home()


if __name__ == "__main__":
    application.secret_key = urandom(12)
    application.run(host=host, port=port)
