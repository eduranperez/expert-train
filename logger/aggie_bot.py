import json
import ldap
import re

def log_event(event, context):
    # TODO implement
    print("Aggie Bot is logging slack event")
    print(event)

    print('Got message')
    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")
    kb_regex = re.compile("KB[0-9]+")
    ldap_regex = re.compile("^ldap")

    if kb_regex.match(text):
        pass#post_kb_link(channel_id, text)
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

    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }

