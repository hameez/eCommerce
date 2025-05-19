from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
import app.crud.product_crud as crud
from app.schemas import ProductCreate, ProductResponse

router = APIRouter()


@router.get("/products/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return crud.get_products(db)


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return crud.get_product(db, product_id)


@router.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)


@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return crud.delete_product(db, product_id)
