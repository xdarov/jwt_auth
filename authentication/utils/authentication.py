import re
import hashlib
from fastapi import HTTPException
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from db_models import User


class PasswordChecker:
    def __init__(self, password):
        self.password = password
        self.is_valid()

    def is_valid(self):
        if len(self.password) < 8:
            raise HTTPException(
                status_code=400, detail="Пароль менее 8 символов")
        if not re.search(r"[!@#$%^&*]", self.password):
            raise HTTPException(
                status_code=400, detail="Пароль должен содержать спецсимволы (!@#$%^&*)")
        if not any(char.isupper() for char in self.password):
            raise HTTPException(
                status_code=400, detail="Пароль должен содержать заглавную букву")


def username_already_exists_interceptor(func):
    async def wraper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (UniqueViolation, IntegrityError) as e:
            print("first", e)
            raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")
    return wraper


def hash_password(password) -> str:
    password_bytes = password.encode('utf-8')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password_bytes)
    hashed_password = sha256_hash.hexdigest()
    return hashed_password


def is_valid_password(user: User, password) -> bool:
    return user and user.password == hash_password(password)
