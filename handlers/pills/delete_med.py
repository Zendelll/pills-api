from aiohttp import web
from internal.responses import json_response
from internal.param_validator import validate
from internal.logger import logger
from internal.db import delete_med as delete
from internal.db import get_med

async def delete_med(request: web.BaseRequest):
    """удалить препарат
    
    Params: login - логин юзера, name - название препарата
    """
    param = await request.json()
    if not validate(param, ["login", "name"]): return json_response(400)
    if not get_med(param['login'], param['name']): 
        logger.error(f"Пользователя {param['login']} нет в базе или у него нет препарата {param['name']}")
        return json_response(404)
    
    if not delete(param['login'], param['name']):
        logger.error(f"Что-то пошло не так в delete_med login = {param['login']}, med = {param['name']}")
        return json_response(500)
    logger.debug(f"Препарат успешно удален из бд login = {param['login']}, med = {param['name']}")
    return json_response(200)