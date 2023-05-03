from aiohttp import web
from internal.responses import json_response
from internal.param_validator import validate
from internal.logger import logger
import logic.pills as pills

async def delete_med(request: web.BaseRequest):
    """удалить препарат
    
    login - логин юзера, name - название препарата
    """
    param = await request.json()
    db = pills.open_json()
    if not validate(param, ["login", "name"]): return json_response(400)
    if param["login"] not in db: 
        logger.error(f'Пользователя {param["login"]} нет в базе')
        return json_response(404)

    result = {}
    for med, cont in db[param["login"]].items():
        if med != param["name"]:
            result[med] = cont
    db[param["login"]] = result
    pills.write_json(db)
    return json_response(200)