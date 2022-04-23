from ampalibe import webserver

from typing import Optional
from pydantic import BaseModel

from fastapi.security import OAuth2PasswordBearer

from model.user import UserModel, Login, History

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    password: Optional[str] = None
    user_id: Optional[int] = None
    token: Optional[str] = None
    lang: Optional[str] = None


class Attachment(BaseModel):
    name: str
    status: Optional[str] = None
    user_id: int = None


@webserver.post('/roso/api/login')
async def login(user: User):
    # res = UserModel.login(user.username, user.password, user.token)
    res = {
        "username": user.username,
        "password": user.password,
    }
    return res


@webserver.post('/roso/api/add_user')
async def add_user(user: User):
    # res = UserModel.login(user.username, user.password, user.token)
    res = {
        "username": user.username,
        "password": user.password,
        "user_id": user.user_id,
    }
    return res


@webserver.post('/roso/api/add_user')
async def send_file(attachement: Attachment):
    res = {
        "name": attachement.name,
        "status": attachement.status,
        "user_id": attachement.user_id,
    }
    return res
