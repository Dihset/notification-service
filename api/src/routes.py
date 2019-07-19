from aiohttp import web
from .views import handler

urls = [
    web.get('/', handler)
]