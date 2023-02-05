from handlers.tg_bot import get_me

def setup_routes(app):
    app.router.add_get('/', get_me)
    app.router.add_get('/tg/getme', get_me)