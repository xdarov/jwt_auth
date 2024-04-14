import os
import aiohttp
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from schemas import UserSchema

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AUTH_HOST = os.environ.get("AUTH_HOST", 'localhost')
AUTH_PORT = os.environ.get("AUTH_PORT", '8100')

url_registration = f"http://{AUTH_HOST}:{AUTH_PORT}/registration"
url_authentication = f"http://{AUTH_HOST}:{AUTH_PORT}/authentication"
url_authorization = f"http://{AUTH_HOST}:{AUTH_PORT}/authorization"

jwt_cookie_names = ("access_token", "refresh_token", "token_type")


@app.get("/")
async def get_html_file(request: Request):
    root_path = "static"
    file_path = os.path.join(root_path, 'index.html')

    return FileResponse(file_path)


@app.get("/index.css")
async def get_css_file(request: Request):
    root_path = "static"
    file_path = os.path.join(root_path, 'index.css')
    
    return FileResponse(file_path)


@app.get("/index.js")
async def get_js_file(request: Request):
    root_path = "static"
    file_path = os.path.join(root_path, 'index.js')
    
    return FileResponse(file_path)


@app.post("/registration")
async def registration(request: Request, user_schema: UserSchema):
    async with aiohttp.ClientSession() as session:
        async with session.post(url_registration, json=user_schema.model_dump()) as response:
            if response.status == 200:
                resp = JSONResponse(content={"detail": "success"})
                for key, value in (await response.json()).items():
                    resp.set_cookie(key=key, value=value, httponly=True)
            else:
                resp = JSONResponse(content=await response.json(), status_code=response.status)
    return resp


@app.post("/authentication")
async def authentication(request: Request, user_schema: UserSchema):
    async with aiohttp.ClientSession() as session:
        async with session.post(url_authentication, json=user_schema.model_dump()) as response:
            if response.status == 200:
                resp = JSONResponse(content={"detail": "success"})
                for key, value in (await response.json()).items():
                    resp.set_cookie(key=key, value=value, httponly=True)
            else:
                resp = JSONResponse(content=await response.json(), status_code=response.status)
    return resp


@app.post("/authorization")
async def authorization(request: Request):
    cockies = request._cookies
    async with aiohttp.ClientSession() as session:
        async with session.post(url_authorization, json=cockies) as response:
            if response.status == 200:
                resp = JSONResponse(content={"detail": "success"})
                response_data = await response.json()
                if response_data:
                    for key, value in response_data.items():
                        resp.set_cookie(key=key, value=value, httponly=True)
            else:
                resp = JSONResponse(content=await response.json(), status_code=response.status)
    return resp


@app.post("/log_out")
async def log_out(request: Request): 
    resp = JSONResponse(content={"detail": "success"})
    for name in jwt_cookie_names:
        resp.set_cookie(name, '')
    return resp

