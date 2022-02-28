import asyncio
import hashlib
import string
from dataclasses import dataclass

import aiohttp
from asyncache import cached
from cachetools import TTLCache


@dataclass
class User:
    studentid: int
    album: str
    imie: str
    nazwisko: str
    
    @staticmethod
    def from_dict(d: dict):
        return User(
            studentid=d.get("studentid"),
            album=d.get("album"),
            imie=d.get("imie"),
            nazwisko=d.get("nazwisko"),
        )


@dataclass
class WdToken:
    studentid: int
    wdauth: str
    expiry_epoch_s: int


class UnauthorizedError(BaseException):
    def __str__(self) -> str:
        return "Wrong username or password :/"


class UnknownError(BaseException):
    pass


class UserService:
    async def login_user(album: str, password: str) -> WdToken:
        _hash = await hash_password(password)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://wdauth.wsi.edu.pl/authenticate?album={album}&pass={_hash}"
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return WdToken(
                        studentid=data["token"]["studentid"],
                        wdauth=data["token"]["wdauth"],
                        expiry_epoch_s=data["token"]["expiry_epoch_s"],
                    )
                elif resp.status == 401:
                    raise UnauthorizedError
                else:
                    raise UnknownError

    @cached(TTLCache(100, 180))
    async def get_user(token: str) -> User:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://wdauth.wsi.edu.pl/user?wdauth={token}"
            ) as resp:
                resp.raise_for_status()
                if resp.status == 200:
                    data = await resp.json()
                    return User.from_dict(data)


async def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


async def main():
    token: WdToken = await UserService.login_user(
        "kurs01", "CA"
    )  # 5ccec052-6b47-4ceb-9a46-36e71301157a
    print(token)
    user: User = await UserService.get_user(token.wdauth)
    print(user)
    print(user.studentid)


if __name__ == "__main__":
    asyncio.run(main())
