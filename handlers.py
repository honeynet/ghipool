#!/usr/bin/python3

from urllib.parse import urlencode

import aiohttp
import tornado.web
from tornado.escape import json_encode

from utils import coroutine


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *args):
        super(BaseHandler, self).__init__(*args)
        print(self.request.path)


class MainHandler(BaseHandler):
    def get(self):
        with open('index.html', 'rb') as fh:
            self.write(fh.read())


class AckHandler(BaseHandler):
    @coroutine
    def get(self):
        code = self.get_argument('code', None)
        state = self.get_argument('state', None)
        resp = yield from aiohttp.request(
            'POST',
            'https://github.com/login/oauth/access_token',
            params={
                'client_id': self.application.gh_client_id,
                'client_secret': self.application.gh_client_secret,
                'code': code
            },
            headers={'Accept': 'application/json'}
        )
        data = yield from resp.json()
        if state == self.application.gh_state:
            issue_url = '/issues?' + urlencode({'token': data['access_token']})
            self.redirect(issue_url)


class SynHandler(BaseHandler):
    def get(self):
        params = {
            'client_id': self.application.gh_client_id,
            'state': self.application.gh_state
        }
        url = 'https://github.com/login/oauth/' + 'authorize?' + urlencode(params)
        self.redirect(url)


class IssuesHandler(BaseHandler):
    @coroutine
    def get(self):
        data = []
        token = self.get_argument('token', None)
        if token:
            resp = yield from aiohttp.request(
                'GET',
                'https://api.github.com/repos/glastopf/conpot/issues',
                params={
                    'access_token': token
                },
                headers={'Accept': 'application/json'}
            )
            data = yield from resp.json()
        else:
            resp = yield from aiohttp.request(
                'GET',
                'https://api.github.com/repos/glastopf/conpot/issues',
                params={
                    'client_id': self.application.gh_client_id,
                    'client_secret': self.application.gh_client_secret
                },
                headers={'Accept': 'application/json'}
            )
            data = yield from resp.json()
        self.write(json_encode(data))
