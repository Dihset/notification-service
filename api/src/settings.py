import pathlib
import logging
import os
import configparser


#Default
PROJECT_DIR = pathlib.Path(__file__).parent.parent

#Logger
logging.basicConfig(level=logging.DEBUG)

#Database

#AMQP
QUEUE_NAME = os.getenv('QUEUE_NAME', 'mail')

#database_config = config['database']
#client = motor.motor_asyncio.AsyncIOMotorClient(
#    database_config['host'],
#    int(database_config['port'])
#)
#db = client['admin_panel_for_life']
