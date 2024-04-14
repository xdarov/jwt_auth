import hashlib
from datetime import datetime
from collections import defaultdict


class UserSessionVersion:
    sessions = defaultdict(defaultdict)

    def __init__(self, session_hash_name, version) -> None:
        self.session = session_hash_name
        self.version = version

    @staticmethod
    def get_session_hash(username: str) -> str:
        session_name = f"{username}{datetime.now()}".encode('utf-8')
        sha256_hash = hashlib.sha256()
        sha256_hash.update(session_name)
        return sha256_hash.hexdigest()

    @classmethod
    def get_session_version(cls, username: str, session_hash_name: str) -> int | None:
        return cls.sessions.get(username, {}).get(session_hash_name)

    @classmethod
    def remove_user_sessions(cls, username: str):
        cls.sessions[username] = defaultdict()

    @classmethod
    def create_session(cls, username: str):
        session_hash_name = cls.get_session_hash(username)
        cls.sessions[username][session_hash_name] = 1
        return cls(session_hash_name, cls.sessions[username][session_hash_name])

    @classmethod
    def set_new_session_version(cls, username: str, session_hash_name: str):
        cls.sessions[username][session_hash_name] += 1
        return cls(session_hash_name, cls.sessions[username][session_hash_name])

    @classmethod
    def check_session_version(cls, token_username, token_session, token_version):
        version = cls.get_session_version(token_username, token_session)

        if version != token_version:
            cls.remove_user_sessions(token_username)

        return version == token_version
