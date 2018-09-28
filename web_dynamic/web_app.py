#!/usr/bin/env python3

from flask import Flask, render_template, url_for, redirect, flash, session, request, abort
from uuid import uuid4
from os import getenv, urandom
from flask_login import LoginManager, current_user, login_user
from models import User
from GoogleAPIKey import APIKey


application = Flask(__name__)
application.url_map.strict_slashes = False
port = int(getenv('HBNB_API_PORT', '5001'))
host = '0.0.0.0'
login = LoginManager(application)


@application.route('/')
def home():
    '''
        main page of app without login
    '''
    return render_template('index.html', APIKey=APIKey)


@application.route('/login', methods=['POST'])
def login():
    req = request.form.to_dict()
    user = User.objects.get(email=req['email'])
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

@application.route("/uuu")
def uuu():
    return session['userId']


if __name__ == "__main__":
    application.secret_key = urandom(12)
    application.run(host=host, port=port)
