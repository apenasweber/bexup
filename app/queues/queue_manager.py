from app.queues.queue_utils import enqueue_message, dequeue_message


def send_brand_to_queue(brand):
    """
    Envia uma marca para a fila para ser processada pela API-2.
    """
    queue_name = "brand_queue"
    enqueue_message(queue_name, brand)


def process_brands_from_queue(callback):
    """
    Processa as marcas da fila. A função callback é chamada para cada marca.
    """
    queue_name = "brand_queue"
    dequeue_message(queue_name, callback)
