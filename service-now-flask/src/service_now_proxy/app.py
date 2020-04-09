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
    data = request.form
    text = data['text']
    s = pysnow.Client(
        instance=SN_INSTANCE_URL,
        user=SN_USERNAME,
        password=SN_PASSWORD) 
    needit = s.resource(api_path='/table/x_58872_needit_needit') 
    record = needit.get(query={'number':text})
    if record:
        return jsonify(record.one()), 200
    else:
        return jsonify({'message': 'Record not found'})

def slack_action():
    """Log slack action."""
    data = request.json
    logging.info(data)
    if data and 'challenge' in data:
        return jsonify({'challenge': data['challenge']})
    else:
        return Response(status=200)

def create_app():
    """Initialize app."""
    app = Flask(__name__)
    app.add_url_rule('/health', view_func=health, methods=['GET'])
    app.add_url_rule('/needits', view_func=needits, methods=['GET', 'POST'])
    app.add_url_rule('/slack', view_func=slack_action, methods=['GET','POST'])
    return app
