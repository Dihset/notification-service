from aiohttp.web import json_response, middleware, HTTPNotFound
from schematics.exceptions import DataError
from bson.errors import InvalidId


@middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except DataError as error:
        return json_response(
            {'error': error.to_primitive()},
            status=400
        )
    except InvalidId as error:
        return json_response(
            {'error': str(error)},
            status=400
        )
    except HTTPNotFound as error:
        return json_response(
            {'error': str(error)},
            status=404
        )
