import boto3
import json
import os
import pika
import sys
from botocore.exceptions import ClientError

# Ensure proper env vars set
RABBIT_HOST = os.environ['RABBIT_HOST']
MAIL_QUEUE = os.environ['MAIL_QUEUE']
AWS_REGION = os.environ['AWS_REGION']

client = boto3.client('ses',region_name=AWS_REGION)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
    channel = connection.channel()

    channel.queue_declare(queue=MAIL_QUEUE)

    def callback(ch, method, properties, body):
        data = json.loads(body)
        print("Received",data)
        sender = data['sender']
        recipients = data['recipients']
        subject = data['subject']
        body = data['body']
        charset = data.get('charset', 'UTF-8')

        try:
            response = client.send_email(
                Destination={
                    'ToAddresses': recipients,
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': charset,
                            'Data': body,
                        },
                        'Text': {
                            'Charset': charset,
                            'Data': body,
                        },
                    },
                    'Subject': {
                        'Charset': charset,
                        'Data': body,
                    },
                },
                Source=sender,
            ) 
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])

        # We can callback to original service, do db operations etc

    channel.basic_consume(queue=MAIL_QUEUE, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)