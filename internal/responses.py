from aiohttp import web

def json_response(status: int):
    errors = {
        "200": {
            "message": "OK",
            "status": 200
        },
        "400": {
            "message": "Bad payload",
            "status": 400
        },
        "404": {
            "message": "Not found",
            "status": 404
        }
    }
    return web.json_response(data={"message": errors[str(status)]["message"]}, status=errors[str(status)]["status"])