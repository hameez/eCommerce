from pydantic import BaseModel
from datetime import datetime

from app.models import ProductCategories


class ProductCreate(BaseModel):
    name: str
    sku: str
    description: str
    price: float
    created_at: datetime
    updated_at: datetime
    category_ids: list[int]


class ProductResponse(BaseModel):
    id: int
    name: str
    sku: str
    description: str
    price: float
    created_at: datetime
    updated_at: datetime
    category_ids: list[int]

    @classmethod
    def from_orm(cls, product, db):
        category_ids = (
            db.query(ProductCategories.category_id)
            .filter(ProductCategories.product_id == product.id)
            .all()
        )

        category_id_list = [c[0] for c in category_ids]  # Extract IDs

        return cls(
            id=product.id,
            name=product.name,
            sku=product.sku,
            description=product.description,
            price=product.price,
            created_at=product.created_at,
            updated_at=product.updated_at,
            category_ids=category_id_list  # ✅ Use category IDs
        )


class SalesCreate(BaseModel):
    product_id: int
    quantity: int
    total_amount: float
    sale_date: datetime


class SalesResponse(SalesCreate):
    id: int


class InventoryUpdate(BaseModel):
    product_id: int
    stock_quantity: int
    last_updated: datetime
    low_stock_alert: bool


class InventoryTransactionCreate(BaseModel):
    product_id: int
    quantity_change: int
    previous_stock_quantity: int
    new_stock_quantity: int
    transaction_type: str
    transaction_date: datetime


class InventoryTransactionResponse(BaseModel):
    id: int
    product_id: int
    product_name: str  # ✅ Include product name
    quantity_change: int
    previous_stock_quantity: int
    new_stock_quantity: int
    transaction_type: str
    transaction_date: datetime


class CategoryBase(BaseModel):
    name: str
    description: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    name: str | None = None
    description: str | None = None


class CategoryResponse(CategoryBase):
    id: int
