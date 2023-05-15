from pydantic import BaseModel


class Client(BaseModel):
    id: int
    name: str
    phone: str
    district: str
    street: str
    number: int
    due: float
    user_id: int


class ClientCreate(BaseModel):
    name: str
    phone: str
    district: str
    street: str
    number: int
    due: float
    user_id: int
