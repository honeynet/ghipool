#!/usr/bin/python3

import os

from uuid import uuid4

import tornado.httpserver
import tornado.ioloop
import tornado.netutil
import tornado.web
import tornado.platform.asyncio

import asyncio

import handlers
from utils import create_self_signed_cert


CERT_FILE = 'selfsigned.crt'
KEY_FILE = 'private.key'
if not len(set(os.listdir('.')).intersection([KEY_FILE, CERT_FILE])) == 2:
    create_self_signed_cert(CERT_FILE, KEY_FILE)


class Application(tornado.web.Application):
    def __init__(self, handlers, **settings):
        tornado.web.Application.__init__(self, handlers, **settings)
        self.gh_client_id = ''
        self.gh_client_secret = ''
        self.gh_state = str(uuid4())


if __name__ == '__main__':
    tornado.platform.asyncio.AsyncIOMainLoop().install()
    app = Application(
        [
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static/'}),
            (r'/', handlers.MainHandler),
            (r'/ack', handlers.AckHandler),
            (r'/syn', handlers.SynHandler),
            (r'/issues', handlers.IssuesHandler),
        ],
        cookie_secret=str(uuid4()),
        #login_url='/login',
        #xsrf_cookies=True
    )
    sockets = tornado.netutil.bind_sockets(8080)
    server = tornado.httpserver.HTTPServer(app, ssl_options={
        'certfile': CERT_FILE,
        'keyfile': KEY_FILE,
    })
    server.add_sockets(sockets)

    asyncio.get_event_loop().run_forever()
