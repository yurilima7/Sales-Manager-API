from fastapi import FastAPI
from routes.auth_routes import auth_router
from routes.client_routes import client_router
from routes.sale_routes import sale_router
from routes.user_routes import user_router

app = FastAPI()


app.include_router(auth_router)
app.include_router(client_router)
app.include_router(sale_router)
app.include_router(user_router)
