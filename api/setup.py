#!/usr/bin/env python
from aiohttp import web
from src.app import init_app
from src.settings import *


if __name__ == "__main__":
    app = init_app()
    web.run_app(app)
