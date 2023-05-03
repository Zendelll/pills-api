import datetime as tm
from datetime import datetime
from aiohttp import web
from internal.responses import json_response
from internal.param_validator import validate
from internal.logger import logger
import logic.pills as pills

async def pills_count(request: web.BaseRequest):
    """Сколько осталось таблеток и до какого числа
    
    login - логин юзера
    """
    db = pills.open_json()
    if not validate(request.rel_url.query, ["login"]): return json_response(400)
    login = request.rel_url.query["login"]
    if not (login in db) or not db[login]: 
        logger.error(f'Пользователя {login} нет в базе')
        return json_response(404)

    result = {}
    for name, cont in db[login].items():
        try:
            date = datetime.strptime(db[login][name]["date"], '%Y-%m-%d')
            now = datetime.today()
            delta = now - date
            real_count = db[login][name]["count"] - (delta.days * db[login][name]["pills_use"])
            real_count = real_count if real_count > 0 else 0
            db[login][name]["count"] = real_count
            db[login][name]["date"] = datetime.today().strftime('%Y-%m-%d')
            pills.write_json(db)
            result[name] = (datetime.today() + tm.timedelta(days=int(real_count/db[login][name]["pills_use"]))).strftime('%Y-%m-%d')
        except:
            continue
    return json_response(200, result)