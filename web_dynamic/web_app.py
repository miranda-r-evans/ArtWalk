#!/usr/bin/env python3
'''
    web app
'''

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
def home():
    '''
        main page of app without login
    '''
    return render_template('index.html', APIKey=APIKey)


@application.route('/loginpage')
def loginpage():
    '''
        page users use to log in
    '''
    if session.get('logged_in') is True:
        return home()
    return render_template('login.html', APIKey=APIKey)


@application.route('/login', methods=['POST'])
def login():
    '''
        login route that login information is sent to and session is started
    '''
    if request.method == 'GET':
        return home()

    try:
        req = request.form.to_dict()
        user = User.objects.get(email=req['email'])
    except StopIteration:
        abort(400)

    if user.verify_password(req['password']) is True:
        session['logged_in'] = True
        session['userId'] = str(user.id)
    else:
        flash('wrong password!')
    return home()


@application.route('/logout')
def logout():
    '''
        log out route
    '''
    session['logged_in'] = False
    session.pop('userId')
    return home()


@application.route('/newwalk', methods=['POST'])
def newwalk():
    '''
        likes or saves a new route
    '''
    req = request.form.to_dict()
    action = req['action']
    req.pop('action')

    try:
        userId = session['userId']
    except KeyError:
        abort(404)

    try:
        req['keywords'] = req['keywords'].split(',')
    except KeyError:
        req['keywords'] = []
    req['waypoints'] = req['waypoints'].split(',')

    req['likes'] = 0
    print(req)
    if action == 'like':
        walkroute = requests.post('http://127.0.0.1:5000/api/v1/walkingroutes', json=req, headers={'Content-Type': 'application/json'})
        requests.put('http://127.0.0.1:5000/api/v1/usersroutes/liked/' + userId, json={'route_id': walkroute.json()['id']}, headers={'Content-Type': 'application/json'})
    else:
        walkroute = requests.post('http://127.0.0.1:5000/api/v1/walkingroutes', json=req, headers={'Content-Type': 'application/json'})
        requests.put('http://127.0.0.1:5000/api/v1/usersroutes/saved/' + userId, json={'route_id': walkroute.json()['id']}, headers={'Content-Type': 'application/json'})

    return '', 204

@application.route('/existingwalk', methods=['POST'])
def existingwalk():
    '''
        likes or saves an existing route
    '''
    req = request.form.to_dict()
    action = req['action']
    req.pop('action')

    try:
        userId = session['userId']
    except KeyError:
        abort(404)

    if action == 'like':
        requests.put('http://127.0.0.1:5000/api/v1/usersroutes/liked/' + userId, json={'route_id': req['id']}, headers={'Content-Type': 'application/json'})
    else:
        requests.put('http://127.0.0.1:5000/api/v1/usersroutes/saved/' + userId, json={'route_id': req['id']}, headers={'Content-Type': 'application/json'})
    
    return '', 204

@application.route('/myroutes')
def myroutes():
    '''
        displays a user's routes
    '''
    try:
        userId = session['userId']
    except KeyError:
        abort(404)

    walkroutes = requests.get('http://127.0.0.1:5000/api/v1/usersroutes/saved/' + userId).json()
    return render_template('saved.html', APIKey=APIKey, walkroutes=walkroutes)


@application.route('/recommended')
def recommended():
    '''
        displays popular routes
    '''
    walkroutes = requests.get('http://127.0.0.1:5000/api/v1/walkingroutes').json()

    return render_template('recommended.html', APIKey=APIKey, walkroutes=walkroutes)

@application.route('/custom')
def custom():
    '''
        lets a user design a custom route
    '''
    return render_template('custom.html', APIKey=APIKey)


if __name__ == "__main__":
    application.secret_key = urandom(12)
    application.run(host=host, port=port)
