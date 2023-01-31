from handlers.tg_bot import get_me

def setup_routes(app):
    app.router.add_post('/tg/getme', get_me)