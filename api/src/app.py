from aiohttp import web
from aiohttp_swagger import *
from .middlewares import error_middleware
from .routes import urls



def init_app():
    """App factory"""
    app = web.Application(
        middlewares=[
            error_middleware,
        ]
    )
    app.add_routes(urls)
    setup_swagger(app, swagger_url='/api/swagger')
    return app
