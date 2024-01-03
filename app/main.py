from fastapi import FastAPI
from pymongo import MongoClient

from model import User, ProductDB, Product, ProductList
from db import connect

app = FastAPI()
conn = connect()
cursor = conn.cursor()

# Replace with your url
client = MongoClient('mongodb://localhost:27017')
product_db = client.product_catalog
product_collection = product_db.products


def initialize_db():
    conn = connect()
    cursor = conn.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        password VARCHAR(255)
    )
    """
    cursor.execute(query)
    conn.close()


@app.on_event("startup")
async def startup_event():
    initialize_db()


@app.post("/register_user")
async def register_user(user: User):
    conn = connect()
    cursor = conn.cursor()
    query = """
            insert into user(name,password) values(
            """
    query += "'" + user.name + "'," + "'" + user.password + "')"
    print(query)
    cursor.execute(query)
    conn.commit()
    conn.close()
    return {"result": "success"}


@app.post("/products", response_model=ProductDB)
async def create_product(product: Product):
    new_product = product_collection.insert_one(product.model_dump())
    return {**product.model_dump(), "id": str(new_product.inserted_id)}


@app.get("/products", response_model=ProductList)
async def list_products():
    products = list(product_collection.find())
    return {"products": products}


@app.get("/product_details")
async def list_products(name: str):
    product = product_collection.find({"name": name})
    return {"product_details": product}
