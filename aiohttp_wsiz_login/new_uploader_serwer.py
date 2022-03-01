from asyncio import sleep
from cgitb import html
from fileinput import filename
from genericpath import exists
from importlib.resources import path
import os
from random import randint
import wd_login
import ownershipstore
from ownershipstore import OwnershipStore

from aiohttp import request, web
import aiohttp.hdrs
from aiohttp.abc import BaseRequest
from faker import Faker

routes = web.RouteTableDef()

# pip install aiohttp

"""
query = req.match_info.get('query', '')  # for route-resolving, /{query}
query = req.rel_url.query['query']  # params; required; else .get('query','default')
"""


@routes.get("/")
async def hello(request):
    print("request received")
    return web.json_response({"comment": f"hello, x={12}!"})


@routes.get("/welcome")
async def welcome(request):
    name = request.rel_url.query["name"]
    await sleep(1.2)
    print(f"welcome request received for {name}")
    return web.json_response({"comment": f"hello {name}!"})


@routes.get("/users/{userid}/details")
async def welcome(request):
    # http://0.0.0.0:8888/users/i8811/details
    userid = request.match_info.get("userid", "")
    fake = Faker()
    user_name = fake.name()
    user_address = fake.address().replace("\n", ", ")
    resp = {"userid": userid, "name": user_name, "address": user_address}
    return web.json_response(resp)


@routes.get("/serve")  # działa, zwrocic uwage na cwd
async def serve_file(request: web.Request):
    token: str = request.rel_url.query.get("token")
    try:
        await wd_login.UserService.get_user(token)
    except:
        raise web.HTTPUnauthorized()
    current_user: wd_login.User = await wd_login.UserService.get_user(token)
    filename = request.rel_url.query.get("filename", "")
    if await OwnershipStore().can_read(filename, current_user.studentid) == False:
        raise web.HTTPForbidden()
    print(filename)
    path = os.path.join("images", filename)
    if (
        ".." in filename
        or "/" in filename
        or "\\" in filename
        or not os.path.isfile(path)
    ):
        raise RuntimeError("Invalid filename")
    return web.FileResponse(path)


@routes.get("/upload")
async def upload_file(req: web.Request):
    # https://everything.curl.dev/http/multipart
    return web.Response(
        text="""<form action="upload" method="post" enctype="multipart/form-data">
  Name: <input type="text" name="person"><br>
  File: <input type="file" name="secret"><br>
  <input type="submit" value="Submit">
</form>""",
        content_type="text/html",
    )


@routes.post("/upload")  # to do token
async def accept_file(req: BaseRequest):
    """
    Funkcja przyjmująca upload pliku.
    """
    # https://docs.aiohttp.org/en/stable/web_quickstart.html#file-uploads
    # token: str = request.headers.get("token")
    # try:
    #     await wd_login.UserService.get_user(token)
    # except:
    #     raise web.HTTPUnauthorized()
    # print("file upload request hit...")

    reader = await req.multipart()
    async for part in reader:
        if part is None:
            break
        else:
            print(f"part {part.name} content_type: {part.headers}")
        # print(await part.text())
        if part.name == "secret":
            with open(part.filename, "wb") as wf:
                file_as_bytes = b""
                while True:
                    chunk = await part.read_chunk()  # 8192 bytes by default.
                    print(type(chunk))
                    if not chunk:
                        break
                    # size += len(chunk)
                    file_as_bytes += chunk
                wf.write(file_as_bytes)

    return web.json_response({"name": "dupa"})


async def starter():
    """
    Starter / app factory, czyli miejsce gdzie można inicjalizować asynchronicze konstrukty.
    """
    await sleep(0.2)
    print("app is starting..")
    # await database.connect()
    return app


app = web.Application()
app.add_routes(routes)
web.run_app(starter(), port=8888)  # ewentu


## Invoke-WebRequest -Headers @{"token" = "56a4620e-404a-468d-b7dc-1b5b6365c186"} -Uri "http://localhost:8888/serve?filename=kaczka.png"
