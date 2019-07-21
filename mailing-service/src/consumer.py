import logging
import json
import datetime
from email.mime.text import MIMEText
from .settings import SMTP_USERNAME


async def send_email_consumer(smtp, scheduler, queue):
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                email = parse_message(message)
                scheduler.add_job(
                    send_email,
                    'date',
                    run_date=email['date'],
                    args=[smtp, email],
                    id=email['_id']
                )


async def send_email(smtp, data):
    message = MIMEText("Sent via aiosmtplib")
    message["From"] = SMTP_USERNAME
    message["To"] = data['email']
    message["Subject"] = data['text']
    await smtp.send_message(message)
    logging.info('OK')


def parse_message(message):
    data = message.body.decode()
    data = json.loads(data)
    data['date'] = datetime.datetime.strptime(
        data['date'],
        '%Y-%m-%dT%H:%M:%S.%f'
    )
    return data
