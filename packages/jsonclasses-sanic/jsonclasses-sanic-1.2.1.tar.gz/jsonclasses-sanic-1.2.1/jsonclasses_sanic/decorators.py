from functools import wraps
from .middlewares import (only_accept_middleware, only_respond_middleware,
                          only_handle_middleware, only_accept_json_middleware,
                          only_respond_json_middleware)
from .utils import recursive_snake_keys

def only_accept(content_types):
    def only_accept_content_type(handler):
        @wraps(handler)
        async def wrapped(request, *args, **kwargs):
            await only_accept_middleware(content_types)(request)
            return await handler(request, *args, **kwargs)
        return wrapped
    return only_accept_content_type


def only_respond(content_types):
    def only_respond_content_type(handler):
        @wraps(handler)
        async def wrapped(request, *args, **kwargs):
            await only_respond_middleware(content_types)(request)
            return await handler(request, *args, **kwargs)
        return wrapped
    return only_respond_content_type


def only_handle(content_types):
    def only_handle_content_type(handler):
        @wraps(handler)
        async def wrapped(request, *args, **kwargs):
            await only_handle_middleware(content_types)(request)
            return await handler(request, *args, **kwargs)
        return wrapped
    return only_handle_content_type


def only_accept_json(handler):
    @wraps(handler)
    async def wrapped(request, *args, **kwargs):
        await only_accept_json_middleware(request)
        return await handler(request, *args, **kwargs)
    return wrapped


def only_respond_json(handler):
    @wraps(handler)
    async def wrapped(request, *args, **kwargs):
        await only_respond_json_middleware(request)
        return await handler(request, *args, **kwargs)
    return wrapped


def only_handle_json(handler):
    @wraps(handler)
    async def wrapped(request, *args, **kwargs):
        await only_accept_json_middleware(request)
        await only_respond_json_middleware(request)
        return await handler(request, *args, **kwargs)
    return wrapped


def underscore_request_json(handler):
    @wraps(handler)
    async def wrapped(request, *args, **kwargs):
        request.parsed_json = recursive_snake_keys(request.json)
        return await handler(request, *args, **kwargs)
    return wrapped
