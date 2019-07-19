from aiohttp import web


def handler(request):
    return web.Response(text='Hello')
    