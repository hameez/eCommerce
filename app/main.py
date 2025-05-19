from fastapi import FastAPI
from app.routers import products, categories, inventory, sales

app = FastAPI()

app.include_router(products.router)
app.include_router(categories.router)
app.include_router(inventory.router)
app.include_router(sales.router)
