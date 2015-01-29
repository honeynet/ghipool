#!/usr/bin/python3

import asyncio
from aiohttp import web

import handlers


@asyncio.coroutine
def init(event_loop):
    app = web.Application(loop=event_loop)
    app.router.add_route('GET', '/projects', handlers.ProjectHandler(event_loop).handle_projects)
    app.router.add_route('GET', '/projects_data', handlers.ProjectsDataHandler(event_loop).handle_projects_data)
    app.router.add_route('GET', '/', handlers.IndexHandler(event_loop).handle_index)
    app.router.add_route('GET', '/static/{folder}/{file_name}', handlers.StaticHandler(event_loop).handle_static)

    srv = yield from event_loop.create_server(app.make_handler(), '127.0.0.1', 8080)
    print("Server started at http://127.0.0.1:8080")
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
