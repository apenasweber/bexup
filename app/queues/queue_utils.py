import pika
import json
from app.core.settings import settings

RABBITMQ_HOST = settings.RABBITMQ_HOST

_connection = None
_channel = None


def get_connection():
    global _connection
    if _connection is None or _connection.is_closed:
        _connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST)
        )
    return _connection


def get_channel():
    global _channel
    if _channel is None or _channel.is_closed:
        _channel = get_connection().channel()
    return _channel


def enqueue_message(queue_name, message_body):
    channel = get_channel()
    channel.queue_declare(queue=queue_name, durable=True)

    message = json.dumps(message_body)
    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2),
    )


def dequeue_message(queue_name, callback):
    channel = get_channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
