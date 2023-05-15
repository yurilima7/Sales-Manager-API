from fastapi import APIRouter, Body, HTTPException

from auth.auth import authenticate, create_access_token, create_refresh_token, create_account

auth_router = APIRouter()


@auth_router.post("/login")
async def login(email: str = Body(...), password: str = Body(...)):
    user = await authenticate(email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    access_token = await create_access_token(user["email"])
    refresh_token = await create_refresh_token(user["email"])
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@auth_router.post("/register")
async def register(name: str = Body(...), email: str = Body(...), password: str = Body(...)):
    await create_account(name, email, password)
    return {"message": "Usuário criado com sucesso"}
