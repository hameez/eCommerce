from sqlalchemy.orm import Session
from app.models import Inventory, InventoryTransaction, Product
from datetime import datetime


# Get inventory status including low-stock alerts
def get_inventory_status(db: Session):
    return db.query(Inventory).all()


# Update inventory levels and track changes
def update_inventory(db: Session, product_id: int, quantity_change: int, transaction_type: str):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if not inventory:
        return {"error": "Product not found in inventory"}

    previous_stock = inventory.stock_quantity
    new_stock = previous_stock + quantity_change

    inventory.stock_quantity = new_stock
    inventory.low_stock_alert = new_stock < 10
    inventory.last_updated = datetime.now()

    db.commit()

    # Log transaction
    transaction = InventoryTransaction(
        product_id=product_id,
        quantity_change=quantity_change,
        previous_stock_quantity=previous_stock,
        new_stock_quantity=new_stock,
        transaction_type=transaction_type,
        transaction_date=datetime.utcnow()
    )
    db.add(transaction)
    db.commit()

    return inventory


def get_inventory_transactions(db: Session):
    transactions = (
        db.query(
            InventoryTransaction.id,
            InventoryTransaction.product_id,
            Product.name.label("product_name"),
            InventoryTransaction.quantity_change,
            InventoryTransaction.previous_stock_quantity,
            InventoryTransaction.new_stock_quantity,
            InventoryTransaction.transaction_type,
            InventoryTransaction.transaction_date
        )
        .join(Product, InventoryTransaction.product_id == Product.id)
        .all()
    )

    return [dict(t._mapping) for t in transactions]
