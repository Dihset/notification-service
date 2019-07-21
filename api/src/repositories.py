from abc import ABCMeta, abstractmethod
from bson.objectid import ObjectId
from aiohttp.web import HTTPNotFound
from .models import Notification


class NotificationSource(metaclass=ABCMeta):

    @abstractmethod
    async def get_all(self, page=0, limit=10): pass

    @abstractmethod
    async def get_by_id(self, pk): pass

    @abstractmethod
    async def save(self, obj: Notification): pass

    @abstractmethod
    async def delete(self, pk): pass

    @abstractmethod
    async def update(self, pk, fields_dict): pass


class NotificationRepository:

    def __init__(self, source: NotificationSource):
        self.source = source

    async def get_all(self, page=0, limit=10):
        return await self.source.get_all(page, limit)

    async def get_by_id(self, pk):
        return await self.source.get_by_id(pk)

    async def save(self, obj: Notification):
        return await self.source.save(obj)

    async def delete(self, pk):
        return await self.source.delete(pk)

    async def update(self, pk, fields_dict):
        return await self.source.update(pk, fields_dict)


class NotificationMongoSource(NotificationSource):

    def __init__(self, db):
        self.db = db
        self.collection = self.db['notification']

    async def get_all(self, page=0, limit=10):
        count = await self.collection.count_documents({})
        if page*limit > count:
            raise HTTPNotFound(text='Page not found')
        cursor = self.collection.find(skip=page*limit, limit=10)
        return [self._mongo_obj_to_dict(document) for document in await cursor.to_list(length=10)]

    async def get_by_id(self, pk):
        result = await self.collection.find_one({
            '_id': ObjectId(pk)
        })
        if not result:
            raise HTTPNotFound(text='Notification not found.')
        return self._mongo_obj_to_dict(result)

    async def save(self, obj: Notification):
        result = await self.collection.insert_one(obj.to_primitive())
        return str(result.inserted_id)

    async def delete(self, pk):
        result = await self.get_by_id(pk)
        await self.collection.delete_one({
            '_id': ObjectId(pk)
        })
        return result

    async def update(self, pk, fields_dict):
        pass

    def _mongo_obj_to_dict(self, obj):
        obj['_id'] = str(obj['_id'])
        return obj
