import requests
import datetime as tm
from datetime import datetime
from aiohttp import web
import json
import os
import sys
from internal.responses import json_response
from internal.param_validator import validate
import logic.pills as pills

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
async def get_info(request: web.BaseRequest):
    db = open_json(f"{DB_PATH}db.json")
    if not validate(request.rel_url.query, "login", str): return json_response(400)
    if not (request.rel_url.query["login"] in db) or not (db[request.rel_url.query["login"]]): return json_response(404)
    return await pills.get_info(request.rel_url.query["login"])

#сколько осталось таблеток и до какого числа
#login - логин юзера
async def pills_count(request: web.BaseRequest):
    db = open_json(f"{DB_PATH}db.json")
    if not validate(request.rel_url.query, "login", str): return json_response(400)
    login = request.rel_url.query["login"]
    if not (login in db) or not db[login]: return json_response(404)

    result = {}
    for name, cont in db[login].items():
        try:
            date = datetime.strptime(db[login][name]["date"], '%Y-%m-%d')
            now = datetime.today()
            delta = now - date
            real_count = db[login][name]["count"] - (delta.days * db[login][name]["pills_use"])
            real_count = real_count if real_count > 0 else 0
            db[login][name]["count"] = real_count
            db[login][name]["date"] = datetime.today().strftime('%Y-%m-%d')
            write_json(f"{DB_PATH}db.json", db)
            result[name] = (datetime.today() + tm.timedelta(days=int(real_count/db[login][name]["pills_use"]))).strftime('%Y-%m-%d')
        except:
            continue
    return json_response(200, result)

#Подсчет, до какого числа хватит таблеток, если добавить add_pills таблеток к текущим
#login - логин юзера, name - название препарата, add_pills - сколько таблеток добавится (число от 0 до 10000)
async def pills_safe_count(request: web.BaseRequest):
    db = open_json(f"{DB_PATH}db.json")
    param = request.rel_url.query
    if not (validate(param, "login", str) and validate(param, "name", str) and validate(param, "add_pills", str)): return json_response(400)
    login = param["login"]
    name = param["name"]
    add_pills = int(param["add_pills"])
    if not (login in db and name in db[login]): return json_response(404)
    if add_pills > 10000 or add_pills < 0: return json_response(400)

    date = datetime.strptime(db[login][name]["date"], '%Y-%m-%d')
    now = datetime.today()
    delta = now - date
    real_count = db[login][name]["count"] - (delta.days * db[login][name]["pills_use"])
    real_count = real_count if real_count > 0 else 0
    db[login][name]["count"] = real_count
    db[login][name]["date"] = datetime.today().strftime('%Y-%m-%d')
    write_json(f"{DB_PATH}db.json", db)
    result = datetime.today() + tm.timedelta( days=( int( (real_count+add_pills)/db[login][name]["pills_use"] ) ) )
    return json_response(200, {"Последний день": result.strftime('%Y-%m-%d')})

#добавить новый препарат
#login - логин юзера, name - название препарата, count - количество таблеток, pills_use - количество таблеток в день
async def set_med(request: web.BaseRequest):
    param = await request.json()
    db = open_json(f"{DB_PATH}db.json")
    #Проверка наличия параметров и соответвие их типу
    if not (validate(param, "login", str) and validate(param, "name", str) and validate(param, "pills_use", int) and validate(param, "count", int)): return json_response(400)
    if param["login"] not in db: db[param["login"]] = {}

    pill = {"count": param["count"], "pills_use": param["pills_use"], "date": datetime.today().strftime('%Y-%m-%d')}
    db[param["login"]][param["name"]] = pill
    write_json(f"{DB_PATH}db.json", db)
    return json_response(200)

async def user_state(request: web.BaseRequest):
    param = await request.json()
    db = open_json(f"{DB_PATH}db.json")
    #Проверка наличия параметров и соответвие их типу
    if not (validate(param, "login", str) and validate(param, "state", str) ): return json_response(400)
    if param["login"] not in db: db[param["login"]] = {}
    db[param["login"]]["user_state"] = param["state"]
    write_json(f"{DB_PATH}db.json", db)
    return json_response(200)

#удалить препарат
#login - логин юзера, name - название препарата
async def delete_med(request: web.BaseRequest):
    param = await request.json()
    db = open_json(f"{DB_PATH}db.json")
    if not (validate(param, "login", str) and validate(param, "name", str)):  return json_response(400)
    if param["login"] not in db: return json_response(404)

    result = {}
    for med, cont in db[param["login"]].items():
        if med != param["name"]:
            result[med] = cont
    db[param["login"]] = result
    write_json(f"{DB_PATH}db.json", db)
    return json_response(200)

#Добавить количество таблеток + посчитать оставшиеся с прошлой даты
#login - логин юзера, name - название препарата, count - количество новых таблеток
async def add_pills(request: web.BaseRequest):
    param = await request.json()
    db = open_json(f"{DB_PATH}db.json")
    if not (validate(param, "login", str) and validate(param, "name", str) and validate(param, "count", int)): return json_response(400)
    if param["login"] not in db or param["name"] not in db[param["login"]]: return json_response(404)

    date = datetime.strptime(db[param["login"]][param["name"]]["date"], '%Y-%m-%d')
    now = datetime.today()
    delta = now - date
    real_count = db[param["login"]][param["name"]]["count"] - (delta.days * db[param["login"]][param["name"]]["pills_use"])
    real_count = real_count if real_count > 0 else 0
    real_count += param["count"]
    if real_count > 50000: return json_response(400)

    db[param["login"]][param["name"]]["count"] = real_count
    db[param["login"]][param["name"]]["date"] = datetime.today().strftime('%Y-%m-%d')
    write_json(f"{DB_PATH}db.json", db)
    return json_response(200)