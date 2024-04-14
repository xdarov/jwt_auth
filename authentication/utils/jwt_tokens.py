import jwt
from jwt.exceptions import PyJWTError
from datetime import datetime
from utils.token_version import UserSessionVersion


SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 30 * 60
REFRESH_TOKEN_EXPIRE_SECONDS = 60 * 60 * 24 * 7


def create_token(data: dict, expires_delta):
    to_encode = data.copy()
    expire = datetime.now().timestamp() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_tokens(username: str, user_session: UserSessionVersion):
    access_token = create_token(
        data={"sub": username, "session": user_session.session, "version": user_session.version},
        expires_delta=ACCESS_TOKEN_EXPIRE_SECONDS
    )
    refresh_token = create_token(
        data={"sub": username, "session": user_session.session, "version": user_session.version},
        expires_delta=REFRESH_TOKEN_EXPIRE_SECONDS
    )
    return access_token, refresh_token


# ================================================================
def check_expired(token_exp):
    current_time = datetime.now().timestamp()
    # print(current_time, token_exp)
    return token_exp and current_time < token_exp



def verify_token(token: str) -> tuple[bool, str, str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_username = payload.get("sub")
        token_exp = payload.get("exp")
        token_session = payload.get("session")
        token_version = payload.get("version")

        # print(payload)
        # print(check_expired(token_exp))
        # print(UserSessionVersion.check_session_version(token_username, token_session, token_version))
        verify_res = check_expired(token_exp) and \
            UserSessionVersion.check_session_version(token_username, token_session, token_version)

        return verify_res, token_username, token_session
    except PyJWTError as e:
        print("JWT verification failed:", e)
        return False, '', ''
# ================================================================
