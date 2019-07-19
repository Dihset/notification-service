from aiohttp import web
from aiohttp.web import json_response
from .models import Notification


class NotificationListView(web.View):

    async def get(self):
        pass

    async def post(self):
        """
        ---
        summary: Create notification
        description: This end-point allow to test that service is up.
        tags:
        - Notification
        produces:
        - application/json
        responses:
            "201":
                description: Successful operation. Return created object.
        """
        data = await self.request.json()
        notification = Notification(data)
        notification.validate()
        return json_response(
            notification.to_primitive(),
            status=201
        )
 

class NotificationView(web.View):

    async def get(self):
        return json_response({'data': 'data'})

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
