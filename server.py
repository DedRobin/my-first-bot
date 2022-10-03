from json import JSONDecodeError

from aiohttp import web
from marshmallow import ValidationError

from schemas import MessageSchema
from services import send_message

routes = web.RouteTableDef()


@routes.post("/")
async def index_get(request: web.Request) -> web.Response:
    try:
        payload = await request.json()
    except JSONDecodeError:
        return web.json_response({"status": "Request data is invalid"})

    try:
        schema = MessageSchema()
        data = schema.load(payload)
    except ValidationError as e:
        return web.json_response({"status": "Validation Error", "error": e.messages})

    await send_message(data.get("message"), data.get("chat_id"))
    return web.json_response({"status": "OK"})


if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, port=5000)
