from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str
    totalVendido: float
    recebido: float
    receber: float


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    totalVendido: float
    recebido: float
    receber: float
