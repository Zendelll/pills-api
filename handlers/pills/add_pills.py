from datetime import datetime
from aiohttp import web
from internal.responses import json_response
from internal.param_validator import validate
from internal.logger import logger
from internal.db import set_med
from internal.db import get_med

MAX_PILL_COUNTER = 5000

async def add_pills(request: web.BaseRequest):
    """Добавить количество таблеток + посчитать оставшиеся с прошлой даты
    
    Params: login - логин юзера, name - название препарата, count - количество новых таблеток
    """
    param = await request.json()
    if not validate(param, ["login", "name", "count"]): return json_response(400)
    med = get_med(param['login'], param['name'])
    if not med:
        logger.error(f"Пользователя {param['login']} нет в базе или у него нет препарата {param['name']}")
        return json_response(404)

    date = datetime.strptime(f"{med.last_count_date}", '%Y-%m-%d')
    now = datetime.today()
    delta = now - date
    pills_counter = med.amount - delta.days * med.daily_usage
    pills_counter = pills_counter if pills_counter > 0 else 0
    pills_counter += param["count"]
    if pills_counter > MAX_PILL_COUNTER: return json_response(400)

    if not set_med(param['login'], param['name'], med.daily_usage, pills_counter):
        logger.error(f"Что-то пошло не так в add_pills login = {param['login']}, med = {param['name']}, pill_counter = {pills_counter}, adding_amount = {param['count']}")
        return json_response(500)
    return json_response(200)