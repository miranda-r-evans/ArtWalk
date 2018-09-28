from api.v1.views import app_views
from flask import jsonify, request


@app_views.route('/status', methods=['GET'])
def status():
    '''
        route to check if api is working
    '''
    return jsonify({"status": "OK"})
