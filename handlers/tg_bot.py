import requests
from aiohttp import web
import json
import os
import sys

async def get_me(request):
    return web.json_response({"answ": "Alive!!"})