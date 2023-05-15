from fastapi import APIRouter, HTTPException, Depends

from auth.auth import get_current_user
from database.database import create_sale, get_sale, get_all_sales, get_all_sales_client, update_sale, patch_total, \
    delete_sale
from models.sale import SaleCreate

sale_router = APIRouter()


@sale_router.post("/sale")
async def register_sale(sale_info: SaleCreate, current_user: dict = Depends(get_current_user)):
    sale_id = await create_sale(sale_info)
    sale_registered = await get_sale(sale_id)
    return sale_registered


@sale_router.get("/sale/{sale_id}")
async def sale(sale_id: int, current_user: dict = Depends(get_current_user)):
    sale_registered = await get_sale(sale_id)
    if sale_registered is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale_registered


@sale_router.get("/sale-user/{user_id}")
async def all_sales_users(user_id: int, current_user: dict = Depends(get_current_user)):
    sales = await get_all_sales(user_id)
    return sales


@sale_router.get("/sale-client/{client_id}")
async def all_sales_users(client_id: int, current_user: dict = Depends(get_current_user)):
    sales = await get_all_sales_client(client_id)
    return sales


@sale_router.put("/sale/{sale_id}")
async def update_client_existing(sale_id: int, sale_registered: SaleCreate,
                                 current_user: dict = Depends(get_current_user)):
    sale_mod = await update_sale(sale_id, sale_registered)
    if sale_mod is None:
        raise HTTPException(status_code=404, detail="Sale not found")

    sale_registered_mod = await get_sale(sale_id)
    return sale_registered_mod


@sale_router.patch("/sale/{sale_id}")
async def update_due_client(sale_id: int, sale_registered: dict, current_user: dict = Depends(get_current_user)):
    sale_mod = await patch_total(sale_id, sale_registered)
    if sale_mod is None:
        raise HTTPException(status_code=404, detail="Sale not found")

    sale_registered_mod = await get_sale(sale_id)
    return sale_registered_mod


@sale_router.delete("/sale/{sale_id}")
async def delete_sale_existing(sale_id: int, current_user: dict = Depends(get_current_user)):
    sale_mod = await delete_sale(sale_id)
    if sale_mod is None:
        raise HTTPException(status_code=404, detail="Sale not found")

    return {"message": "Compra deletada com sucesso"}
