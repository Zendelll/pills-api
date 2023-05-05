import datetime as tm
from datetime import datetime
from aiohttp import web
from internal.responses import json_response
from internal.param_validator import validate
from internal.logger import logger
from internal.db import get_user_meds
from internal.db import set_med

async def pills_count(request: web.BaseRequest):
    """Сколько осталось таблеток и до какого числа
    
    login - логин юзера
    """
    if not validate(request.rel_url.query, ["login"]): return json_response(400)
    login = request.rel_url.query["login"]
    meds = get_user_meds(login)
    if not meds:
        logger.error(f"Пользователя {login} нет в базе")
        return json_response(404)

    result = {}
    for line in meds:
        date = datetime.strptime(f"{line.last_count_date}", '%Y-%m-%d')
        now = datetime.today()
        delta = now - date
        pills_counter = line.amount - delta.days * line.daily_usage
        pills_counter = pills_counter if pills_counter > 0 else 0
        if not set_med(login, line.med_name, line.daily_usage, pills_counter):
            logger.error(f"Что-то пошло не так в pills_count login = {login}, med = {line.med_name}, pill_counter = {pills_counter}")
            return json_response(500)
        if pills_counter == 0:
            result[line.med_name] = "Уже кончились"
        else:
            result[line.med_name] = (datetime.today() + tm.timedelta(days=int(pills_counter/line.daily_usage))).strftime('%d-%m-%Y')
    return json_response(200, result)