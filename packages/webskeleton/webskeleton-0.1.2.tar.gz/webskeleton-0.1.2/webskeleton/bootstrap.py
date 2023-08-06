import asyncio
from inspect import getmembers, isfunction
import json
import logging
from types import ModuleType

from aiohttp import web  # type: ignore

from . import appredis
from . import db
from .env import ENV
from .typez import Req


async def handle_json(req: Req, handler) -> web.Response:
    response_body = None
    try:
        response_body = await handler(req)
    except web.HTTPException as e:
        return web.Response(status=e.status, text=e.text)
    res = web.Response()
    if getattr(response_body, "_asdict", None):  # a namedtuple
        res.text = json.dumps(response_body._asdict())
    else:
        res.text = json.dumps(response_body)
    for action in req.reply_operations:
        getattr(res, action.fn)(*action.args, **action.kwargs)
    for key, val in req.reply_headers:
        res.headers[key] = val
    return res


def req_wrapper_factory():
    @web.middleware
    async def wrap_req(request, handler):
        req = Req(wrapped=request)
        return await handle_json(req, handler)

    return wrap_req


def setup_logging(level=logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s.%(msecs)03d "
        "%(levelname)s %(module)s - %(funcName)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return


# public
def load_routes(webapp: web.Application, routes_mod: ModuleType) -> web.Application:
    METHOD_MAP = {
        "GET": web.get,
        "POST": web.post,
        "PUT": web.put,
    }
    fns = [
        f
        for name, f in getmembers(routes_mod)
        if isfunction(f) and getattr(f, "is_endpoint", None)
    ]
    routes = [METHOD_MAP[fn.method](fn.path, fn) for fn in fns]  # type: ignore
    logging.info("loaded routes:\n%s", "\n".join(map(str, routes)))
    webapp.add_routes(routes)
    return webapp


class WebSkeleton:
    def __init__(self, routes_module: ModuleType):
        setup_logging(ENV.LOG_LEVEL)
        self.routes_module = routes_module
        return

    async def _startup_services(self):
        await db.connect()
        await appredis.connect()
        return

    async def _load_app(self):
        await self._startup_services()
        app = web.Application(middlewares=[req_wrapper_factory()])
        app = load_routes(app, self.routes_module)
        return app

    async def run_async(self):
        app = await self._load_app()
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", ENV.PORT)
        logging.info("starting on port %s", ENV.PORT)
        await site.start()
        return

    def run(self):
        import uvloop  # type: ignore

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

        logging.info("starting on port %s", ENV.PORT)
        web.run_app(self._load_app(), port=ENV.PORT)
        return
