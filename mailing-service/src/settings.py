import os
import pathlib
import logging


#Default
PROJECT_DIR = pathlib.Path(__file__).parent.parent

#logging
logging.basicConfig(level=logging.DEBUG)

#smtp
SMTP_HOSTNAME = os.getenv('SMTP_HOSTNAME', 'smtp.gmail.com')
SMTP_PORT = os.getenv('SMTP_PORT', 587)
SMTP_USERNAME = os.getenv('SMTP_USERNAME', 'slamihin123@gmail.com')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', 'animeforgay')

#amqp
QUEUE_NAME = os.getenv('QUEUE_NAME', 'mail')
