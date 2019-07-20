import os
from motor import motor_asyncio


async def create_mongo(app):
    db = motor_asyncio.AsyncIOMotorClient(
        f'mongodb://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@mongo'
    )[os.environ['DB_NAME']]
    app['db'] = db
