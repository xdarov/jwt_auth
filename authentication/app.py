from fastapi import FastAPI, Request, Response, HTTPException, Cookie
from fastapi.responses import JSONResponse
from handlers import create_user, check_user, check_authorization
from schemas import UserSchema, JWTSchema
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


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


@app.post("/registration")
async def registration(request: Request, user: UserSchema):
    print(request.__dict__)
    access_token, refresh_token = await create_user(user)
    response = JSONResponse({"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"})
    return response


@app.post("/authentication")
async def authentication(request: Request, user: UserSchema):
    access_token, refresh_token = await check_user(user)
    response = JSONResponse({"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"})
    return response


@app.post("/authorization")
async def authorization(request: Request, tokens: JWTSchema):
    response = check_authorization(tokens)
    return response