#!/usr/bin/env python3

from api.v1.views import app_views
from flask import Flask
from flask_cors import CORS, cross_origin
from os import getenv
import models

application = Flask(__name__)
application.url_map.strict_slashes = False
host = getenv('HOST', '0.0.0.0')
port = int(getenv('PORT', '5000'))
application.register_blueprint(app_views)
cors = CORS(application, resources={r'/api/v1/*': {'origins': '*'}})

if __name__ == "__main__":
    application.run(host=host, port=port)
