from abc import ABCMeta, abstractmethod
from bson.objectid import ObjectId
from aiohttp.web import HTTPNotFound
from .models import Notification


class NotificationSource(metaclass=ABCMeta):

    @abstractmethod
    async def get_all(self): pass

    @abstractmethod
    async def get_by_id(self, pk): pass

    @abstractmethod
    async def save(self, obj: Notification): pass

    @abstractmethod
    async def delete(self, pk): pass

    @abstractmethod
    async def update(self): pass


class NotificationRepository:

    def __init__(self, source: NotificationSource):
        self.source = source

    async def get_all(self):
        return await self.source.get_all()

    async def get_by_id(self, pk):
        return await self.source.get_by_id(pk)

    async def save(self, obj: Notification):
        return await self.source.save(obj)

    async def delete(self, pk):
        return await self.source.delete(pk)

    async def update(self):
        return await self.source.update()


class NotificationMongoSource(NotificationSource):

    def __init__(self, db):
        self.db = db
        self.collection = self.db['notification']

    async def get_all(self):
        pass

    async def get_by_id(self, pk):
        result = await self.collection.find_one({
            '_id': ObjectId(pk)
        })
        if not result:
            raise HTTPNotFound(text='Notification not found.')
        result['_id'] = str(result['_id'])
        return result

    async def save(self, obj: Notification):
        result = await self.collection.insert_one(obj.to_primitive())
        return str(result.inserted_id)

    async def delete(self, pk):
        pass

    async def update(self):
        pass
