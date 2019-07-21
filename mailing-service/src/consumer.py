import logging
import aio_pika
from email.mime.text import MIMEText
from .settings import SMTP_USERNAME, QUEUE_NAME


async def send_email_consumer(smtp):
    conn = await aio_pika.connect_robust(
        'amqp://guest:guest@rabbitmq:5672/'
    )
    chan = await conn.channel()
    await chan.set_qos(prefetch_count=1)
    exchange = await chan.declare_exchange(
        'test_incoming',
        type=aio_pika.ExchangeType.DIRECT,
        durable=True,
    )
    dlx_exchange = await chan.declare_exchange(
        'dlx_incoming',
        type=aio_pika.ExchangeType.DIRECT,
        durable=True,
    )
    queue = await chan.declare_queue(
        QUEUE_NAME,
        durable=True,
        arguments={
            'x-message-ttl': 60000,
            'x-dead-letter-exchange': dlx_exchange.name,
        },
    )
    await queue.bind(exchange)
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                logging.info(message.body)



async def send_email(smtp):
    message = MIMEText("Sent via aiosmtplib")
    message["From"] = SMTP_USERNAME
    message["To"] = "zpm09119@bcaoo.com"
    message["Subject"] = "Hello World!"
    await smtp.send_message(message)
    print('OK')
