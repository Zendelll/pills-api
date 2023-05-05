from aiohttp import web
from handlers.pills.get_user_meds import get_user_meds
from handlers.pills.set_med import set_med
from handlers.pills.add_pills import add_pills
from handlers.pills.pills_count import pills_count
from handlers.pills.pills_safe_count import pills_safe_count
from handlers.pills.delete_med import delete_med
from handlers.pills.update_user_state import user_state
from handlers.pills.get_user_state import get_user_state

def setup_routes(app: web.Application):
    app.router.add_get('/pills/get_me', get_user_meds)
    app.router.add_get('/pills/pills_count', pills_count)
    app.router.add_get('/pills/pills_safe_count', pills_safe_count)
    app.router.add_get('/pills/get_user_state', get_user_state)
    app.router.add_post('/pills/add_pills', add_pills)
    app.router.add_put('/pills/user_state', user_state)
    app.router.add_put('/pills/set_med', set_med)
    app.router.add_delete('/pills/delete_med', delete_med)
    