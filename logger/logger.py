import json

def log_event(event, context):
    # TODO implement
    print("Aggie Bot is logging")
    print(event)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Aggie Bot!')
    }