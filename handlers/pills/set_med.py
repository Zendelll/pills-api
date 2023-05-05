from datetime import datetime
from aiohttp import web
from internal.responses import json_response
from internal.param_validator import validate
from internal.logger import logger
from internal.db import set_med as set

async def set_med(request: web.BaseRequest):
    """Добавить новый препарат
    
    login - логин юзера, name - название препарата, count - количество таблеток, pills_use - количество таблеток в день
    """
    param = await request.json()
    if not validate(param, ["login", "name", "pills_use", "count"]): return json_response(400)
    if not set(param['login'], param['name'], param['pills_use'], param['count']):
        logger.error(f"Что-то пошло не так в set_med login = {param['login']}, med = {param['name']}, amount = {param['count']}, daily_usage = {param['pills_use']}")
        return json_response(500)
    logger.debug(f"Препарат успешно добавлен в бд login = {param['login']}, med = {param['name']}")
    return json_response(200)