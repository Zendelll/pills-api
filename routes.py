from aiohttp import web
from handlers.pills import get_info
from handlers.pills import set_med
from handlers.pills import add_pills
from handlers.pills import pills_count
from handlers.pills import pills_safe_count
from handlers.pills import delete_med

def setup_routes(app: web.Application):
    app.router.add_get('/pills/get_me', get_info)
    app.router.add_get('/pills/pills_count', pills_count)
    app.router.add_get('/pills/pills_safe_count', pills_safe_count)
    app.router.add_post('/pills/add_pills', add_pills)
    app.router.add_put('/pills/set_med', set_med)
    app.router.add_delete('/pills/delete_med', delete_med)
    