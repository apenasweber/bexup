import pika
import logging
from app.services.fipe_service import fipe_service as fetch_data_from_fipe

logging.basicConfig(level=logging.INFO)

RABBITMQ_HOST = "localhost"
QUEUE_NAME = "brand_queue"


def callback(ch, method, properties, body):
    try:
        message = body.decode()
        fetch_data_from_fipe(message)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logging.error(f"Failed to process message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()


if __name__ == "__main__":
    main()
