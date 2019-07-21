#import aiosmtplib
#from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .settings import *
from .consumer import send_email_consumer


async def init_app():
    #smtp = await init_smtp()
    #await send_email_consumer(smtp)
    await send_email_consumer('dsgdsf')




#async def init_smtp():
#    smtp = aiosmtplib.SMTP(hostname=SMTP_HOSTNAME, port=SMTP_PORT)
#    await smtp.connect()
#    await smtp.starttls()
#    await smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
#    return smtp
