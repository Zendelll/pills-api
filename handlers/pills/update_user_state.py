from aiohttp import web
from internal.responses import json_response
from internal.param_validator import validate
from internal.logger import logger
from internal.db import update_user_state

async def user_state(request: web.BaseRequest):
    """Изменить стейт юзера - нужно для телеграм бота
    
    login - логин юзера, state - новый стейт
    """
    param = await request.json()
    if not validate(param, ["login", "state"]): return json_response(400)
    if not update_user_state(param['login'], param['state']):
        logger.error(f"Что-то пошло не так в update_user_state login = {param['login']}, state = {param['state']}")
        return json_response(500)
    return json_response(200)