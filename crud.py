from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Item
from faker import Faker

# Create a new item in the database
def create_item(db: Session, name: str, description: str):
    db_item = Item(name=name, description=description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)  # Refresh to get the new id assigned
    return db_item

# Get all items from the database
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()

# Get a single item by its ID
def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

# Update an existing item in the database
def update_item(db: Session, item_id: int, name: str, description: str):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db_item.name = name
        db_item.description = description
        db.commit()
        db.refresh(db_item)
    return db_item

# Delete an item by its ID
def delete_item(db: Session, item_id: int):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

# Seeder function to insert 100+ realistic sample data using Faker
def seed_data(db: Session):
    fake = Faker()
    items = []

    # Generate 100+ fake items
    for _ in range(100):
        item = Item(
            name=fake.catch_phrase(),  # Generates a random product name
            description=fake.text(max_nb_chars=100)  # Generates a random description
        )
        items.append(item)

    # Add all items to the session
    db.add_all(items)
    db.commit()

    return {"message": f"Seeded {len(items)} items successfully!"}

def clear_all_data(db: Session):
    try:
        # Clear data from each table
        db.query(Item).delete()  # Add other tables here if necessary
        db.commit()
        return {"message": "All data cleared successfully!"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}