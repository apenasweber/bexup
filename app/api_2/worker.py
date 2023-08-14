from app.api_2.v1.endpoints.brands import process_brand
from app.queue_utils import dequeue_message
import logging

logger = logging.getLogger(__name__)


async def brand_worker():
    while True:
        if brand := dequeue_message():
            try:
                await process_brand(brand)
            except Exception as e:
                logger.error(f"Failed to process brand {brand}. Error: {e}")
