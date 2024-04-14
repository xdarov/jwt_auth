from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str


class JWTSchema(BaseModel):
    access_token: str = None
    refresh_token: str = None
