from asyncio import sleep
from aiohttp import web
from os import name
from sympy import *

routes = web.RouteTableDef()

# aiohttp ... (pip install aiohttp)
"""
query = req.match_info.get('query', '')  # for route-resolving, /{query}
query = req.rel_url.query['query']  # params; required; else .get('query','default')
"""


@routes.get("/")
async def hello(request):
    n = name()
    print(f"{n.nodename} request received")
    return web.json_response({"comment": f"hello from {n.nodename}!"})


@routes.get("/welcome")
async def hellow(request):
    name = request.rel_url.query["name"]
    await sleep(1.2)
    print(f"welcome request received for {name}")
    return web.json_response({"comment": f"hello {name}!"})


@routes.get("/add")
async def hello_sum(request):
    a = float(request.rel_url.query["a"])
    b = float(request.rel_url.query["b"])
    return web.json_response({"result": a + b})


@routes.get("/is_prime")
async def is_prime(request):
    x = int(request.rel_url.query["x"])
    res = isprime(x)
    return web.json_response(f"number {x} is {res}")

app = web.Application()
app.add_routes(routes)
web.run_app(app, port=4411)
