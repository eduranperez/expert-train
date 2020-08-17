import os
import ldap
import logging
import re
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SERVICE_HUB_URL = "https://servicehub.ucdavis.edu/servicehub?id=ucd_kb_article&sysparm_article={KB_ID}"

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter('c2b1bef81ff70be77d987f287c18160d', "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token='xoxb-191385809328-1266587139413-je50jzTlFEyxIJ9DVLi6gbKT')

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
    print('Got message')
    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")
    kb_regex = re.compile("KB[0-9]+")
    ldap_regex = re.compile("^ldap")

    if kb_regex.match(text):
        post_kb_link(channel_id, text)
    elif ldap_regex.match(text):
        query = text[5:]
        print('Searching LDAP for ' + query)
        l = ldap.initialize("ldap://ldap.ucdavis.edu")
        l.simple_bind_s("","")
        res = l.search_s("ou=People,dc=ucdavis,dc=edu", ldap.SCOPE_SUBTREE, "(|(uid={query})(mail={query})(givenName={query})(sn={query})(cn={query}))".format(query=query))
        print('Found {} ldap results'.format(len(res)))
        message_text = ''
        for user in res:
            user_info = user[1]
            for key, value in user_info.items():
                message_text += '{key} {value}\n'.format(key=key, value=value[0].decode("utf-8"))
        print(message_text)
        message = {
            "channel": channel_id,
            "text": message_text
        }
        slack_web_client.chat_postMessage(**message)

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(port=3000)