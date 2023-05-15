from pydantic import BaseModel


class Sale(BaseModel):
    id: int
    product_name: str
    price: float
    quantity: int
    day: str
    total: float
    client_id: int
    user_id: int


class SaleCreate(BaseModel):
    product_name: str
    price: float
    quantity: int
    day: str
    total: float
    client_id: int
    user_id: int
