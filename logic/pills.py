import requests
import datetime as tm
from datetime import datetime
from aiohttp import web
import json
import os
import sys
from internal.responses import json_response


with open("/usr/src/app/config.json") as f:
        CONF = json.load(f)
DB_PATH = CONF['PATH']['DB_PATH']


def open_json(path):
    with open(path) as f:
        db = json.load(f)
    return(db)

def write_json(path, jsonf):
    with open(path, "w", encoding='utf-8') as f:
        json.dump(jsonf, f)


#получить все о юзере
#login - логин юзера
async def get_info(login: str):
    db = open_json(f"{DB_PATH}db.json")
    return json_response(200, db[login])
