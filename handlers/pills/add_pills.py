from datetime import datetime
from aiohttp import web
from internal.responses import json_response
from internal.param_validator import validate
from internal.logger import logger
import logic.pills as pills

async def add_pills(request: web.BaseRequest):
    """Добавить количество таблеток + посчитать оставшиеся с прошлой даты
    
    login - логин юзера,
    name - название препарата,
    count - количество новых таблеток
    """
    param = await request.json()
    db = pills.open_json()
    if not validate(param, ["login", "name", "count"]): return json_response(400)
    if param["login"] not in db or param["name"] not in db[param["login"]]: 
        logger.error(f'Пользователя {param["login"]} нет в базе или лекарства {param["name"]} нет у этого юзера')
        return json_response(404)

    date = datetime.strptime(db[param["login"]][param["name"]]["date"], '%Y-%m-%d')
    now = datetime.today()
    delta = now - date
    real_count = db[param["login"]][param["name"]]["count"] - (delta.days * db[param["login"]][param["name"]]["pills_use"])
    real_count = real_count if real_count > 0 else 0
    real_count += param["count"]
    if real_count > 50000: return json_response(400)

    db[param["login"]][param["name"]]["count"] = real_count
    db[param["login"]][param["name"]]["date"] = datetime.today().strftime('%Y-%m-%d')
    pills.write_json(db)
    return json_response(200)