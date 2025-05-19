from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import Sales, Product, ProductCategories, Category
from app.schemas import SalesCreate
from sqlalchemy.sql import text


# Create a sale record
def create_sale(db: Session, sale: SalesCreate):
    db_sale = Sales(**sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale


# Retrieve all sales
def get_sales(db: Session):
    return db.query(Sales).all()


# Retrieve sales by date range
def get_sales_by_date_range(db: Session, start_date: str, end_date: str):
    return db.query(Sales).filter(Sales.sale_date.between(start_date, end_date)).all()


# Get revenue by time period
def get_revenue_by_period(db: Session, period: str):
    time_group_map = {
        "daily": func.date(Sales.sale_date),
        "weekly": func.extract('week', Sales.sale_date),
        "monthly": func.extract('month', Sales.sale_date),
        "yearly": func.extract('year', Sales.sale_date),
    }

    group_by_expr = time_group_map.get(period, func.date(Sales.sale_date))

    result = (
        db.query(group_by_expr.label("period"), func.sum(Sales.total_amount).label("total_revenue"))
        .group_by(group_by_expr)
        .all()
    )

    return [dict(period=period_val, total_revenue=total) for period_val, total in result]


# Compare revenue across products
def compare_revenue_by_product(db: Session):
    result = db.query(
        func.sum(Sales.total_amount).label("total_sale"),
        ProductCategories.product_id,
        Product.name
    ).join(
        ProductCategories, Sales.product_id == ProductCategories.product_id
    ).join(
        Product, ProductCategories.product_id == Product.id
    ).group_by(
        ProductCategories.product_id, Product.name
    ).all()

    return [
        {
            "total_sale": row[0],
            "product_id": row[1],
            "product_name": row[2]
        }
        for row in result
    ]


# Compare revenue across categories
def compare_revenue_by_category(db: Session):
    result = db.query(
        Category.name,
        text("SUM(sales.total_amount) as total_revenue")
    ).join(
        ProductCategories, Category.id == ProductCategories.category_id
    ).join(
        Sales, Sales.product_id == ProductCategories.product_id
    ).group_by(
        Category.name
    ).all()

    return [{"category": row[0], "total_revenue": row[1]} for row in result]
