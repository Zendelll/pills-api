from aiohttp import web
from internal.responses import json_response
from internal.param_validator import validate
from internal.logger import logger
from internal.db import get_user_meds as user_meds

async def get_user_meds(request: web.BaseRequest):
    """Получить все таблетки юзера
    
    login - логин юзера
    """
    params = request.rel_url.query
    if not validate(params, ["login"]): return json_response(400)
    meds = user_meds(params["login"])
    result = {}
    for med in meds:
        result[med.med_name] = {"count": med.amount, "pills_use": med.daily_usage, "date": f"{med.last_count_date}"}
    logger.debug(f"Login {params['login']}, get_user_meds = {result}")
    return json_response(200, result)