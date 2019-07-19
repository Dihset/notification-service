from aiohttp import web
from .views import handler, NotificationView, NotificationListView


urls = [
    web.get('/', handler),
    web.view('/api/notifications', NotificationListView),
    web.view('/api/notifications/{pk}', NotificationView),
]
