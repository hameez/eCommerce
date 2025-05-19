from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
import app.crud.inventory_crud as crud

router = APIRouter()



@router.get("/inventory/")
def get_inventory_status(db: Session = Depends(get_db)):
    return crud.get_inventory_status(db)


@router.post("/inventory/update/")
def update_inventory(product_id: int, quantity_change: int, transaction_type: str, db: Session = Depends(get_db)):
    return crud.update_inventory(db, product_id, quantity_change, transaction_type)


@router.get("/inventory/transactions/")
def get_transactions(db: Session = Depends(get_db)):
    return crud.get_inventory_transactions(db)
