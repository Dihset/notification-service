import logging
from aiohttp import web
from aiohttp.web import json_response
from .models import Notification
from .repositories import NotificationRepository, NotificationMongoSource


class NotificationViewMixin(web.View):

    def __init__(self, request):
        super().__init__(request)
        db = self.request.app['db']
        self.repository = NotificationRepository(
            NotificationMongoSource(db)
        )


class NotificationListView(NotificationViewMixin):

    async def get(self):
        pass

    async def post(self):
        data = await self.request.json()
        notification = Notification(data)
        notification.validate()
        result = await self.repository.save(notification)
        return json_response(
            dict(
                _id=result,
                **notification.to_primitive(),
            ),
            status=201
        )
 

class NotificationView(NotificationViewMixin):

    def __init__(self, request):
        super().__init__(request)
        self.obj_id = self.request.match_info['pk']

    async def get(self):
        return json_response(
            await self.repository.get_by_id(self.obj_id)
        )

    async def put(self):
        pass

    async def delete(self):
        pass


async def handler(request):
    """
    ---
    description: This end-point allow to test that service is up.
    tags:
    - Health check
    produces:
    - text/plain
    responses:
        "200":
            description: successful operation. Return "pong" text
        "405":
            description: invalid HTTP Method
    """
    return web.Response(text='Hello')
