import datetime as tm
from datetime import datetime
from aiohttp import web
from internal.responses import json_response
from internal.param_validator import validate
from internal.logger import logger
import logic.pills as pills

async def set_med(request: web.BaseRequest):
    """Добавить новый препарат
    
    login - логин юзера, name - название препарата, count - количество таблеток, pills_use - количество таблеток в день
    """
    param = await request.json()
    db = pills.open_json()
    if not validate(param, ["login", "name", "pills_use", "count"]): return json_response(400)
    if param["login"] not in db: db[param["login"]] = {}

    pill = {"count": param["count"], "pills_use": param["pills_use"], "date": datetime.today().strftime('%Y-%m-%d')}
    db[param["login"]][param["name"]] = pill
    pills.write_json(db)
    return json_response(200)