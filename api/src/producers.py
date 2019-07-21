import json
import aio_pika
from .settings import QUEUE_NAME


async def send_mail_producer(exchange, notification):
    await exchange.publish(
        aio_pika.Message(
            json.dumps(notification.to_primitive()).encode(),
        ),
        routing_key=QUEUE_NAME
    )
