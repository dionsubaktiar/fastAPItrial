from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Item  # Make sure the Item model is imported

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

# Seeder function to insert more realistic sample data
def seed_data(db: Session):
    # Example of more realistic item data
    items = [
        Item(name="Wireless Mouse", description="Ergonomic wireless mouse with Bluetooth connectivity."),
        Item(name="Mechanical Keyboard", description="RGB backlit mechanical keyboard with customizable switches."),
        Item(name="Laptop Stand", description="Adjustable laptop stand for better posture."),
        Item(name="Bluetooth Headphones", description="Noise-canceling Bluetooth headphones with long battery life."),
        Item(name="Smartphone Charger", description="Fast-charging USB-C cable for modern smartphones."),
        Item(name="Gaming Mouse Pad", description="Large mouse pad with non-slip base and smooth surface for gaming."),
        Item(name="External SSD", description="Portable solid-state drive with 1TB storage capacity."),
        Item(name="USB-C Hub", description="Multi-port USB-C hub for connecting multiple devices."),
        Item(name="Phone Case", description="Durable and protective phone case for iPhone 13."),
        Item(name="Smartwatch", description="Fitness tracking smartwatch with heart rate monitor and GPS."),
    ]

    # Add all items to the session
    db.add_all(items)
    db.commit()

    # Refresh the first item to get the inserted data (e.g., ID after insert)
    db.refresh(items[0])

    return {"message": "Seed data inserted successfully!"}

def clear_all_data(db: Session):
    try:
        # Clear data from each table
        db.query(Item).delete()  # Add other tables here if necessary
        db.commit()
        return {"message": "All data cleared successfully!"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}