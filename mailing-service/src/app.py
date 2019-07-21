import aio_pika
import aiosmtplib
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .settings import *
from .consumer import send_email_consumer


async def init_app():
    smtp = await init_smtp()
    queue = await init_queue()
    scheduler = await init_scheduler()
    await send_email_consumer(smtp, scheduler, queue)


async def init_smtp():
    smtp = aiosmtplib.SMTP(hostname=SMTP_HOSTNAME, port=SMTP_PORT)
    await smtp.connect()
    await smtp.starttls()
    await smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
    return smtp


async def init_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.start()
    return scheduler


async def init_queue():
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
    return queue
