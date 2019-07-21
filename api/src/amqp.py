import aio_pika
from .settings import QUEUE_NAME


async def create_amqp(app):
    conn = await aio_pika.connect_robust('amqp://guest:guest@rabbitmq:5672/')
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
    app['exchange'] = exchange
