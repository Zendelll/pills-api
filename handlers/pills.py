import requests
import datetime as tm
from datetime import datetime
from aiohttp import web
import json
import os
import sys

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
    try: 
        result = db[request.rel_url.query["login"]]
        return web.json_response(data=result, status=200)
    except:
        return web.json_response(data={"message": "User not found"}, status=404)

#сколько осталось таблеток и до какого числа
#login - логин юзера
async def pills_count(request: web.BaseRequest):
    db = open_json(f"{DB_PATH}db.json")
    login = request.rel_url.query["login"]
    try: 
        db[login]
    except:
        return web.json_response(data={"message": "User not found"}, status=404)

    result = {}
    for name, cont in db[login].items():
        date = datetime.strptime(db[login][name]["date"], '%Y-%m-%d')
        now = datetime.today()
        delta = now - date
        real_count = db[login][name]["count"] - (delta.days * db[login][name]["pills_use"])
        real_count = real_count if real_count > 0 else 0
        db[login][name]["count"] = real_count
        db[login][name]["date"] = datetime.today().strftime('%Y-%m-%d')
        write_json(f"{DB_PATH}db.json", db)
        result[name] = (datetime.today() + tm.timedelta(days=int(real_count/db[login][name]["pills_use"]))).strftime('%Y-%m-%d')
    return web.json_response(data=result, status=200)

#Подсчет, до какого числа хватит таблеток, если добавить add_pills таблеток к текущим
#login - логин юзера, name - название препарата, add_pills - сколько таблеток добавится
async def pills_safe_count(request: web.BaseRequest):
    db = open_json(f"{DB_PATH}db.json")
    login = request.rel_url.query["login"]
    name = request.rel_url.query["name"]
    add_pills = request.rel_url.query["add_pills"]

    date = datetime.strptime(db[login][name]["date"], '%Y-%m-%d')
    now = datetime.today()
    delta = now - date
    real_count = db[login][name]["count"] - (delta.days * db[login][name]["pills_use"])
    real_count = real_count if real_count > 0 else 0
    db[login][name]["count"] = real_count
    db[login][name]["date"] = datetime.today().strftime('%Y-%m-%d')
    write_json(f"{DB_PATH}db.json", db)

    result = datetime.today() + tm.timedelta( days=( int( (real_count+int(add_pills))/db[login][name]["pills_use"] ) ) )
    return web.json_response(data={"Последний день": result.strftime('%Y-%m-%d')}, status=200)

#добавить новый препарат
#login - логин юзера, name - название препарата, count - количество таблеток, pills_use - количество таблеток в день
async def set_pills(request: web.BaseRequest):
    param = await request.json()
    db = open_json(f"{DB_PATH}db.json")
    if param["login"] not in db:
        db[param["login"]] = {}
    pill = {"count": param["count"], "pills_use": param["pills_use"], "date": datetime.today().strftime('%Y-%m-%d')}
    db[param["login"]][param["name"]] = pill
    write_json(f"{DB_PATH}db.json", db)
    return web.json_response(data={"message": "Ok"}, status=200)

#Добавить количество таблеток + посчитать оставшиеся с прошлой даты
#login - логин юзера, name - название препарата, count - количество новых таблеток
async def add_pills(request: web.BaseRequest):
    param = await request.json()
    db = open_json(f"{DB_PATH}db.json")
    if param["login"] not in db:
        return web.json_response(data={"message": "User not found"}, status=404)
    elif param["name"] not in db[param["login"]]:
        return web.json_response(data={"message": "Pill name not found"}, status=404)
    
    
    date = datetime.strptime(db[param["login"]][param["name"]]["date"], '%Y-%m-%d')
    now = datetime.today()
    delta = now - date
    real_count = db[param["login"]][param["name"]]["count"] - (delta.days * db[param["login"]][param["name"]]["pills_use"])
    real_count = real_count if real_count > 0 else 0
    real_count += param["count"]

    db[param["login"]][param["name"]]["count"] = real_count
    db[param["login"]][param["name"]]["date"] = datetime.today().strftime('%Y-%m-%d')
    write_json(f"{DB_PATH}db.json", db)
    return web.json_response(data={"message": "Ok"}, status=200)