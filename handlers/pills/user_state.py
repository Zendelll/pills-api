import datetime as tm
from datetime import datetime
from aiohttp import web
from internal.responses import json_response
from internal.param_validator import validate
from internal.logger import logger
import logic.pills as pills

async def user_state(request: web.BaseRequest):
    """Изменить стейт юзера - нужно для телеграм бота
    
    login - логин юзера, state - новый стейт
    """
    param = await request.json()
    db = pills.open_json()
    if not validate(param, ["login", "state"]): return json_response(400)
    if param["login"] not in db: db[param["login"]] = {}
    db[param["login"]]["user_state"] = param["state"]
    pills.write_json(db)
    return json_response(200)