import boto3
import json
import logging
import os
import pika
import sys
from botocore.exceptions import ClientError
from foo import foo

# Ensure proper env vars set
AWS_REGION = os.environ['AWS_REGION']
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
MAIL_QUEUE = os.environ['MAIL_QUEUE']
RABBIT_HOST = os.environ['RABBIT_HOST']


class SystemLogFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, 'app_name'):
            record.app_name = 'main'
        return True

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s:%(app_name)s:%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(LOG_LEVEL)
logger.addFilter(SystemLogFilter())

client = boto3.client('ses',region_name=AWS_REGION)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
    channel = connection.channel()

    channel.exchange_declare(exchange='lsit-mailer-production', exchange_type='direct')


    def callback(ch, method, properties, body):
        data = json.loads(body)
        app_name = method.routing_key
        logger.debug("Received {data}".format(data=data), extra={'app_name': app_name})
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
            logger.error(e.response['Error']['Message'], extra={'app_name': app_name})
            # Requeue message to retry at a later time
        else:
            logger.info("SES sent email with ID {id} to {recipients}".format(
                id=response['MessageId'],
                recipients=recipients
            ), extra={'app_name': app_name})
            # We can callback to original service, do db operations etc


    for app_name in ["dss-messenger", "dlc-placement"]:
        channel.queue_declare(queue=app_name)
        channel.queue_bind(
            exchange='lsit-mailer-production',
            queue=app_name,
            routing_key=app_name
        )
        channel.basic_consume(
            queue=app_name, on_message_callback=callback, auto_ack=True
        )

    logger.info(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.warn('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)