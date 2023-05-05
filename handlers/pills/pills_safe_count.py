import datetime as tm
from datetime import datetime
from aiohttp import web
from internal.responses import json_response
from internal.param_validator import validate
from internal.logger import logger
from internal.db import get_med
from internal.db import set_med

async def pills_safe_count(request: web.BaseRequest):
    """Подсчет, до какого числа хватит таблеток, если добавить add_pills таблеток к текущим
    
    login - логин юзера, name - название препарата, add_pills - сколько таблеток добавится (число от 0 до 1000)
    """
    param = request.rel_url.query
    if not validate(param, ["login", "name", "add_pills"]): return json_response(400)
    login = param["login"]
    name = param["name"]
    add_pills = int(param["add_pills"])
    med = get_med(login, name)
    if not med:
        logger.error(f"Пользователя {login} или препарата \"{name}\" нет в базе")
        return json_response(404)

    date = datetime.strptime(f"{med.last_count_date}", '%Y-%m-%d')
    now = datetime.today()
    delta = now - date
    pills_counter = med.amount - (delta.days * med.daily_usage)
    pills_counter = pills_counter if pills_counter > 0 else 0
    if not set_med(login, med.med_name, med.daily_usage, pills_counter):
            logger.error(f"Что-то пошло не так в pills_safe_count login = {login}, med = {med.med_name}, pill_counter = {pills_counter}")
            return json_response(500)
    
    result = datetime.today() + tm.timedelta( days=( int((pills_counter+add_pills)/med.daily_usage) ) )
    return json_response(200, {"Последний день": result.strftime('%d-%m-%Y')})
