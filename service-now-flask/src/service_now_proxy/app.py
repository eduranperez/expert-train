"""flask app to communicate with service now."""
import json
import logging
import os
import pysnow
import requests
import sys
from flask import Flask, request, Response, jsonify

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
    needits = s.resource(api_path='/table/x_58872_needit_needit')
    needit = needits.get(query={'number': text}).one_or_none()
    msg = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ('*Incident Found.*' if needit else '*No records found.*')
                }
            },
            {
              "type": "actions",
              "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Create Ticket",
                        "emoji": False
                    }
                }
              ]
            }
        ]
    }
    return jsonify(msg), 200


def slack_action():
    """Log slack action."""
    data = request.json
    logging.info(data)
    if data and 'challenge' in data:
        return jsonify({'challenge': data['challenge']})
    else:
        return Response(status=200)


def interact():
    """Endpoint to handle user interactions."""
    data = request.form
    for k, v in data.items():
        print(k)
        print(type(v))
    payload = json.loads(data['payload'])
    r = requests.post(
        payload['response_url'],
        json={
            "text": "Thanks for your request, we'll process it and get back to you."
        }
    )
    print(r, r.status_code)
    return Response(status=200)


def create_app():
    """Initialize app."""
    app = Flask(__name__)
    app.add_url_rule('/health', view_func=health, methods=['GET'])
    app.add_url_rule('/needits', view_func=needits, methods=['POST'])
    app.add_url_rule('/slack', view_func=slack_action, methods=['POST'])
    app.add_url_rule('/interact', view_func=interact, methods=['POST'])
    return app
