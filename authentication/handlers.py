from sqlalchemy import select
from fastapi import HTTPException

from utils import PasswordChecker, username_already_exists_interceptor, \
hash_password, is_valid_password, create_tokens, verify_token
from db_models import async_session, User
from schemas import UserSchema, JWTSchema
from utils.token_version import UserSessionVersion


@username_already_exists_interceptor
async def create_user(user_schema: UserSchema):
    username = user_schema.username
    password = user_schema.password
    PasswordChecker(password)

    async with async_session() as session:
            async with session.begin():
                user = User(
                    username=username,
                    password=hash_password(password)
                )
                session.add(user)
    user_session = UserSessionVersion.create_session(user.username)
    return create_tokens(user.username, user_session)


async def check_user(user_schema: UserSchema):
    username = user_schema.username
    password = user_schema.password

    async with async_session() as session:
        async with session.begin():
            user: User | None = (await session.execute(
                select(User).where(User.username == username))).scalar_one_or_none()
            if not is_valid_password(user, password):
                raise HTTPException(status_code=401, detail='Неверные логин или пароль')
    user_session = UserSessionVersion.create_session(user.username)
    return create_tokens(user.username, user_session)


def check_authorization(tokens: JWTSchema):
    if tokens.access_token is None:
        raise HTTPException(status_code=401, detail="Не авторизован")
    acces_res, _, _ = verify_token(tokens.access_token)
    print("access res =>", acces_res)
    if acces_res:
        return {}
    refresh_res, username, session = verify_token(tokens.refresh_token)
    if refresh_res:
        user_session = UserSessionVersion.set_new_session_version(username, session)
        access_token, refresh_token = create_tokens(username, user_session)
        print(user_session.__dict__)
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Не авторизован")
