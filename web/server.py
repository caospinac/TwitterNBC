import asyncio
import os

import pymongo
from sanic.response import json
from sanic import response as sr

from web.core import app, config, db

sem = None


@app.listener("before_server_start")
def init(sanic, loop):
    global sem
    concurrency_per_worker = 4
    sem = asyncio.Semaphore(concurrency_per_worker, loop=loop)


async def bounded_fetch(session, url):
    """ Use session object to perform `get` request on url
    """
    async with sem, session.get(url) as response:
        return await response.json()


@app.route("/")
async def root(request):
    return sr.json({
        'hello': "world"
    })


if __name__ == "__main__":
    from web.api import *

    app.run(**config['APP'])
