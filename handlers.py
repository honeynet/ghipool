#!/usr/bin/python3

import json
import os

import asyncio
import aiohttp
from aiohttp import web


class BaseHandler(object):
    def __init__(self, loop):
        self.loop = loop
        self.projects = dict(
            glastopf=['glastopf', 'conpot'],
            honeynet=['beeswarm', 'apkinspector']
        )
        self.session = aiohttp.TCPConnector()


    @asyncio.coroutine
    def _request_api(self, what, owner, repo, path, callback=lambda x: print(x)):
        base_url = 'https://api.github.com/{0}/{1}/{2}{3}'
        print(base_url.format(what, owner, repo, path))
        r = yield from aiohttp.request(
            'GET',
            base_url.format(what, owner, repo, path),
            connector=self.session,
            headers={'Accept': 'application/json'}
        )
        print(r.status)
        content = yield from r.json()
        return content


class IndexHandler(BaseHandler):
    def handle_index(self, request):
        with open('index.html', 'rb') as fh:
            return web.Response(body=fh.read())


class StaticHandler(BaseHandler):
    def handle_static(self, request):
        folder = request.match_info.get('folder', 'None')
        file_name = request.match_info.get('file_name', 'None')
        if folder in os.listdir('static'):
            if file_name in os.listdir(os.path.join('static', folder)):
                with open(os.path.join('static', folder, file_name), 'rb') as fh:
                    return web.Response(body=fh.read())


class ProjectsDataHandler(BaseHandler):

    @asyncio.coroutine
    def handle_projects_data(self, request):
        # /repos/:owner/:repo/issues
        data = dict()
        for owner, projects in self.projects.items():
            data[owner] = dict()
            ret = yield from self._request_api('orgs', owner, 'repos', '')
            for project in ret:
                if project['name'] in projects:
                    data[owner][project['name']] = project
        return web.Response(body=json.dumps(data).encode('utf-8'))


class ProjectHandler(BaseHandler):

    @asyncio.coroutine
    def handle_projects(self, request):
        # /repos/:owner/:repo/stats/code_frequency
        data = []
        for owner, projects in self.projects.items():
            for project in projects:
                ret = yield from self._request_api('repos', owner, project, '/stats/code_frequency')
                additions = 0
                deletions = 0
                if len(ret) >= 4:
                    for week in ret[-4:]:
                        additions += week[1]
                        deletions += week[2]
                else:
                    additions = 'n/a'
                    deletions = 'n/a'
                data.append(dict(
                    owner=owner,
                    project=project,
                    additions_last_month=additions,
                    deletions_last_month=deletions
                ))
        return web.Response(body=json.dumps(data).encode('utf-8'))
