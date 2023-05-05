from aiohttp import web
from internal.responses import json_response
from internal.param_validator import validate
from internal.logger import logger
from internal.db import get_user_state as user_state

async def get_user_state(request: web.BaseRequest):
    """Получить все таблетки юзера
    
    login - логин юзера
    """
    logger.debug("Я туть")
    params = request.rel_url.query
    if not validate(params, ["login"]): return json_response(400)
    state = user_state(params["login"])
    logger.debug(f"get_user_state = {state}")
    return json_response(200, {"user_state": state})