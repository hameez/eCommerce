from sqlalchemy.orm import Session
from app.models import Product, ProductCategories, Category
from app.schemas import ProductCreate, CategoryCreate, ProductResponse
from app.crud.category_crud import create_category_if_not_exists


def get_products(db: Session):
    products = db.query(Product).all()

    product_list = []
    for product in products:
        category_ids = (
            db.query(ProductCategories.category_id)
            .filter(ProductCategories.product_id == product.id)
            .all()
        )

        category_id_list = [c[0] for c in category_ids]  # Extract IDs

        product_list.append(ProductResponse(
            id=product.id,
            name=product.name,
            sku=product.sku,
            description=product.description,
            price=product.price,
            created_at=product.created_at,
            updated_at=product.updated_at,
            category_ids=category_id_list  # ✅ Correct field name
        ))

    return product_list


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def create_product(db: Session, product: ProductCreate):
    # Create product first
    db_product = Product(
        name=product.name,
        sku=product.sku,
        description=product.description,
        price=product.price,
        created_at=product.created_at,
        updated_at=product.updated_at
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    # Insert product-category mappings in `product_categories`
    for category_id in product.category_ids:
        db_product_category = ProductCategories(product_id=db_product.id, category_id=category_id)
        db.add(db_product_category)

    db.commit()

    # Retrieve linked category IDs
    category_ids = (
        db.query(ProductCategories.category_id)
        .filter(ProductCategories.product_id == db_product.id)
        .all()
    )
    category_id_list = [c[0] for c in category_ids]  # Extract IDs

    # Return the response with category_ids
    return ProductResponse(
        id=db_product.id,
        name=db_product.name,
        sku=db_product.sku,
        description=db_product.description,
        price=db_product.price,
        created_at=db_product.created_at,
        updated_at=db_product.updated_at,
        category_ids=category_id_list
    )


def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product
