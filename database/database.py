import databases as databases
from sqlalchemy import create_engine, MetaData, Column, Integer, Table, String, Float, select
from passlib.context import CryptContext

from models.client import ClientCreate
from models.sale import SaleCreate
from models.user import UserCreate

DATABASE_URL = "sqlite:///database/database.db"

database = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(150)),
    Column("email", String(100)),
    Column("password", String(100)),
    Column("total_vendido", Float),
    Column("recebido", Float),
    Column("receber", Float),
)

client = Table(
    "client",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(150)),
    Column("phone", String(20)),
    Column("district", String(200)),
    Column("street", String(200)),
    Column("number", Integer),
    Column("due", Float),
    Column("user_id", Integer),
)

sale = Table(
    "sale",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("product_name", String(200)),
    Column("price", Float),
    Column("quantity", Integer),
    Column("day", String(100)),
    Column("total", Float),
    Column("client_id", Integer),
    Column("user_id", Integer)
)

metadata.create_all(engine)
pwd_context = CryptContext(schemes=["bcrypt"])


async def create_user(user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    query = users.insert().values(name=user.name, email=user.email, password=hashed_password,
                                  total_vendido=user.totalVendido, recebido=user.recebido, receber=user.receber)

    return await database.execute(query)


async def get_user(user_id: int):
    query = select([users]).where(users.c.id == user_id)
    return await database.fetch_one(query)


async def patch_user(user_id: int, updated_fields: dict):
    query = users.update().where(users.c.id == user_id).values(**updated_fields)
    return await database.execute(query)


async def get_auth_user(email: str):
    query = select([users]).where(users.c.email == email)
    return await database.fetch_one(query)


async def create_client(client_user: ClientCreate):
    query = client.insert().values(name=client_user.name, phone=client_user.phone, district=client_user.district,
                                   street=client_user.street, number=client_user.number, due=client_user.due,
                                   user_id=client_user.user_id)

    return await database.execute(query)


async def get_client(client_id: int):
    query = select([client]).where(client.c.id == client_id)
    return await database.fetch_one(query)


async def get_all_clients(user_id: int):
    query = select([client]).where(users.c.id == user_id)
    return await database.fetch_all(query)


async def update_client(client_id: int, client_user: ClientCreate):
    query = client.update().where(client.c.id == client_id).values(name=client_user.name, phone=client_user.phone,
                                                                   district=client_user.district,
                                                                   street=client_user.street, number=client_user.number,
                                                                   due=client_user.due,
                                                                   user_id=client_user.user_id)

    return await database.execute(query)


async def patch_due(client_id: int, updated_fields: dict):
    query = client.update().where(client.c.id == client_id).values(**updated_fields)
    return await database.execute(query)


async def delete_client(client_id: int):
    query = client.delete().where(client.c.id == client_id)
    return await database.execute(query)


async def create_sale(sale_client: SaleCreate):
    query = sale.insert().values(product_name=sale_client.product_name, price=sale_client.price,
                                 quantity=sale_client.quantity,
                                 day=sale_client.day, total=sale_client.total, client_id=sale_client.client_id,
                                 user_id=sale_client.user_id)

    return await database.execute(query)


async def get_sale(sale_id: int):
    query = select([sale]).where(sale.c.id == sale_id)
    return await database.fetch_one(query)


async def get_all_sales(user_id: int):
    query = select([sale]).where(sale.c.user_id == user_id)
    return await database.fetch_all(query)


async def get_all_sales_client(client_id: int):
    query = select([sale]).where(sale.c.client_id == client_id)
    return await database.fetch_all(query)


async def update_sale(sale_id: int, sale_client: SaleCreate):
    query = sale.update().where(sale.c.id == sale_id).values(product_name=sale_client.product_name,
                                                             price=sale_client.price,
                                                             quantity=sale_client.quantity,
                                                             day=sale_client.day, total=sale_client.total,
                                                             client_id=sale_client.client_id,
                                                             user_id=sale_client.user_id)

    return await database.execute(query)


async def patch_total(sale_id: int, updated_fields: dict):
    query = sale.update().where(sale.c.id == sale_id).values(**updated_fields)
    return await database.execute(query)


async def delete_sale(sale_id: int):
    query = sale.delete().where(sale.c.id == sale_id)
    return await database.execute(query)
