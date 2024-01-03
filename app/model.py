from typing import List

from pydantic import BaseModel


class User(BaseModel):
    name: str
    password: str

class Product(BaseModel):
    name: str
    description: str
    price: float
    stock: int

class ProductDB(Product):
    id: str

class ProductList(BaseModel):
    products: List[ProductDB]