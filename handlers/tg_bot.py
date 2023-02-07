import requests
from aiohttp import web
import json
import os
import sys

with open("/usr/src/app/config.json") as f:
        CONF = json.load(f)
DB_PATH = CONF['PATH']['DB_PATH']

async def get_me(request):
    with open(f"{DB_PATH}db.json") as f:
        db = json.load(f)
    return web.json_response(db)