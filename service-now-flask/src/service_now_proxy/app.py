"""flask app to communicate with service now."""
import logging
import json
import os
import pysnow
import os   
import sys
from flask import Flask, request, Response, jsonify, session

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
application = Flask(__name__)
SN_USERNAME = os.environ['SN_USERNAME']
SN_PASSWORD = os.environ['SN_PASSWORD']
SN_INSTANCE_URL = os.environ['SN_INSTANCE_URL']

def health():
    """Simple health check."""
    return Response(status=200)

def needits():
    """Return all needits."""
    s = pysnow.Client(
        instance=SN_INSTANCE_URL,
        user=SN_USERNAME,
        password=SN_PASSWORD) 
    needit = s.resource(api_path='/table/x_58872_needit_needit') 
    response = needit.get(stream=True)
    data = {'records': []}
    for needit in response.all():
        data['records'].append(needit)
    print(data)
    return jsonify(data['records']), 200

def create_app():
    """Initialize app."""
    app = Flask(__name__)
    app.add_url_rule('/health', view_func=health, methods=['GET'])
    app.add_url_rule('/needits', view_func=needits, methods=['GET'])
    return app
