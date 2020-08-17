import os
import logging
import re
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from onboarding_tutorial import OnboardingTutorial

SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SERVICE_HUB_URL = "https://servicehub.ucdavis.edu/servicehub?id=ucd_kb_article&sysparm_article={KB_ID}"

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token=SLACK_BOT_TOKEN)

onboarding_tutorials_sent = {}

def post_kb_link(channel_id, text):
    kb_id = "KB" + re.sub("[^0-9]", "", text).zfill(7)
    message = {
        "channel": channel_id,
        "text": SERVICE_HUB_URL.format(KB_ID=kb_id)
    }
    response = slack_web_client.chat_postMessage(**message)

@slack_events_adapter.on("message")
def message(payload):
    event = payload.get("event", {})

    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")
    kb_regex = re.compile('KB[0-9]+')

    if kb_regex.match(text):
        post_kb_link(channel_id, text)

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(port=3000)