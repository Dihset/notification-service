from aiohttp.web import json_response, middleware
from schematics.exceptions import DataError


@middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except DataError as error:
        return json_response(
            {'error': error.to_primitive()},
            status=400
        )
