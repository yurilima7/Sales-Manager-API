from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from database.database import get_auth_user, create_user
from jwt import PyJWTError, decode, encode
from datetime import datetime, timedelta

from models.user import UserCreate

SECRET_KEY = "Wd9z7RwXJ5BkQ2fL6e8pY4gN1Cv0KmTa"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"])
security = HTTPBearer()


async def authenticate(email: str, password: str):
    user = await get_auth_user(email)
    if user and pwd_context.verify(password, user["password"]):
        return user

    return None


async def create_account(name: str, email: str, password: str):
    user = await get_auth_user(email)
    if user:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    user_create = UserCreate(
        name=name,
        email=email,
        password=password,
        totalVendido=0.0,
        recebido=0.0,
        receber=0.0
    )
    await create_user(user_create)


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        user = await get_auth_user(email)

        if user is None:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

        return user
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


async def create_access_token(email: str):
    access_token_expires = timedelta(minutes=60)
    return encode(
        {
            "exp": datetime.utcnow() + access_token_expires,
            "sub": email,
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


async def create_refresh_token(email: str):
    refresh_token_expires = timedelta(days=7)
    return encode(
        {
            "exp": datetime.utcnow() + refresh_token_expires,
            "sub": email,
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
