import datetime as tm
from datetime import datetime
from aiohttp import web
from internal.responses import json_response
from internal.param_validator import validate
from internal.logger import logger
import logic.pills as pills

async def pills_safe_count(request: web.BaseRequest):
    """Подсчет, до какого числа хватит таблеток, если добавить add_pills таблеток к текущим
    
    login - логин юзера, name - название препарата, add_pills - сколько таблеток добавится (число от 0 до 1000)
    """
    db = pills.open_json()
    param = request.rel_url.query
    if not validate(param, ["login", "name", "add_pills"]): return json_response(400)
    login = param["login"]
    name = param["name"]
    add_pills = int(param["add_pills"])
    if not (login in db and name in db[login]): 
        logger.error(f'Пользователя {login} нет в базе или лекарства {name} нет у этого юзера')
        return json_response(404)

    date = datetime.strptime(db[login][name]["date"], '%Y-%m-%d')
    now = datetime.today()
    delta = now - date
    real_count = db[login][name]["count"] - (delta.days * db[login][name]["pills_use"])
    real_count = real_count if real_count > 0 else 0
    db[login][name]["count"] = real_count
    db[login][name]["date"] = datetime.today().strftime('%Y-%m-%d')
    pills.write_json(db)
    result = datetime.today() + tm.timedelta( days=( int( (real_count+add_pills)/db[login][name]["pills_use"] ) ) )
    return json_response(200, {"Последний день": result.strftime('%Y-%m-%d')})
