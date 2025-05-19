from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
import app.crud.sales_crud as crud
from app.schemas import SalesCreate, SalesResponse

router = APIRouter()


@router.post("/sales/", response_model=SalesResponse)
def create_sale(sale: SalesCreate, db: Session = Depends(get_db)):
    return crud.create_sale(db, sale)


@router.get("/sales/", response_model=list[SalesResponse])
def get_sales(db: Session = Depends(get_db)):
    return crud.get_sales(db)


@router.get("/sales/revenue/{period}")
def get_revenue(period: str, db: Session = Depends(get_db)):
    return {"revenue": crud.get_revenue_by_period(db, period)}


@router.get("/sales/date-range/")
def get_sales_by_date_range(start_date: str, end_date: str, db: Session = Depends(get_db)):
    return crud.get_sales_by_date_range(db, start_date, end_date)


@router.get("/sales/compare/products")
def compare_revenue_by_product(db: Session = Depends(get_db)):
    return crud.compare_revenue_by_product(db)


@router.get("/sales/compare/categories")
def compare_revenue_by_category(db: Session = Depends(get_db)):
    return crud.compare_revenue_by_category(db)
