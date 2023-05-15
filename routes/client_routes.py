from fastapi import APIRouter, HTTPException, Depends

from auth.auth import get_current_user
from database.database import create_client, get_client, get_all_clients, update_client, delete_client, patch_due
from models.client import ClientCreate

client_router = APIRouter()


@client_router.post("/client")
async def register_client(client_info: ClientCreate, current_user: dict = Depends(get_current_user)):
    client_id = await create_client(client_info)
    client_registered = await get_client(client_id)
    return client_registered


@client_router.get("/client/{client_id}")
async def client(client_id: int, current_user: dict = Depends(get_current_user)):
    client_registered = await get_client(client_id)
    if client_registered is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client_registered


@client_router.put("/client/{client_id}")
async def update_client_existing(client_id: int, client_registered: ClientCreate,
                                 current_user: dict = Depends(get_current_user)):
    client_mod = await update_client(client_id, client_registered)
    if client_mod is None:
        raise HTTPException(status_code=404, detail="Client not found")

    client_registered_mod = await get_client(client_id)
    return client_registered_mod


@client_router.patch("/client/{client_id}")
async def update_due_client(client_id: int, client_registered: dict, current_user: dict = Depends(get_current_user)):
    client_mod = await patch_due(client_id, client_registered)
    if client_mod is None:
        raise HTTPException(status_code=404, detail="Client not found")

    client_registered_mod = await get_client(client_id)
    return client_registered_mod


@client_router.delete("/client/{client_id}")
async def delete_client_existing(client_id: int, current_user: dict = Depends(get_current_user)):
    client_mod = await delete_client(client_id)
    if client_mod is None:
        raise HTTPException(status_code=404, detail="Client not found")

    return {"message": "Cliente deletado com sucesso"}


@client_router.get("/clients/{user_id}")
async def all_clients(user_id: int, current_user: dict = Depends(get_current_user)):
    clients = await get_all_clients(user_id)
    return clients
