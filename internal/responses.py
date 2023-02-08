from aiohttp import web

def json_response(status: int, data = {}):
    statuses = {
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
    if not data:
        return web.json_response(data={"message": statuses[str(status)]["message"]}, status=statuses[str(status)]["status"])
    else:
        return web.json_response(data=data, status=statuses[str(status)]["status"])