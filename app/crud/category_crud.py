from sqlalchemy.orm import Session
from app.models import Category
from app.schemas import CategoryCreate, CategoryUpdate


# Get all categories
def get_categories(db: Session):
    return db.query(Category).all()


# Get a single category
def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


# Create a new category
def create_category(db: Session, category: CategoryCreate):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


# Update a category
def update_category(db: Session, category_id: int, category_data: CategoryUpdate):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category:
        for key, value in category_data.dict(exclude_unset=True).items():
            setattr(category, key, value)
        db.commit()
        db.refresh(category)
    return category


# Delete a category
def delete_category(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category:
        db.delete(category)
        db.commit()
    return category


# Create category (if it doesn't exist)
def create_category_if_not_exists(db: Session, category: CategoryCreate):
    existing_category = db.query(Category).filter(Category.name == category.name).first()
    if existing_category:
        return existing_category  # Return existing category
    new_category = Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category
