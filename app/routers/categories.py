from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
import app.crud.category_crud as crud
from app.schemas import CategoryCreate, CategoryUpdate

router = APIRouter()


@router.get("/categories/")
def get_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)


@router.get("/categories/{category_id}")
def get_category(category_id: int, db: Session = Depends(get_db)):
    return crud.get_category(db, category_id)


@router.post("/categories/")
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, category)


@router.put("/categories/{category_id}")
def update_category(category_id: int, category_data: CategoryUpdate, db: Session = Depends(get_db)):
    return crud.update_category(db, category_id, category_data)


@router.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    return crud.delete_category(db, category_id)
