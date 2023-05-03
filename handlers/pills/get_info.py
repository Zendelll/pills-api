import datetime as tm
from datetime import datetime
from aiohttp import web
from internal.responses import json_response
from internal.param_validator import validate
from internal.logger import logger
import logic.pills as pills

async def get_info(request: web.BaseRequest):
    """Получить все о юзере
    
    login - логин юзера
    """
    db = pills.open_json()
    if not validate(request.rel_url.query, ["login"]): return json_response(400)
    if not (request.rel_url.query["login"] in db) or not (db[request.rel_url.query["login"]]): 
        logger.error(f'Пользователя {request.rel_url.query["login"]} нет в базе')
        return json_response(404)
    return await pills.get_info(request.rel_url.query["login"])