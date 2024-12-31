import shutil
from sqlalchemy.orm import Session
from fastapi import Request
from sqlalchemy import select
from models import Item
from faker import Faker
import random
import os
from urllib.parse import urlencode,urlparse

UPLOAD_DIRECTORY = "./uploaded_images"

def create_item(db: Session, name: str, description: str, price: float, category: str, photo: str):
    if price <= 0:
        raise ValueError("Price must be greater than zero.")
    
    # Validate photo URL format (you can expand this to check if the photo URL is reachable)
    parsed_url = urlparse(photo)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        raise ValueError("Invalid photo URL.")
    
    db_item = Item(name=name, description=description, price=price, category=category, photo=photo)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session, request: Request, page: int = 1, page_size: int = 10):
    """
    Fetch items with pagination and generate next/prev links.
    :param db: Database session
    :param request: FastAPI request object for generating URLs
    :param page: Current page number (1-indexed)
    :param page_size: Number of items per page
    :return: List of items, total count, and pagination links
    """
    total = db.query(Item).count()
    items = (
        db.query(Item)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    # Extract base URL and query parameters
    base_url = str(request.url).split('?')[0]
    query_params = dict(request.query_params)

    # Generate next/prev links
    next_page = None
    if page * page_size < total:
        query_params.update({"page": page + 1, "page_size": page_size})
        next_page = f"{base_url}?{urlencode(query_params)}"
    
    prev_page = None
    if page > 1:
        query_params.update({"page": page - 1, "page_size": page_size})
        prev_page = f"{base_url}?{urlencode(query_params)}"

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,  # Ceiling division
        "next": next_page,
        "prev": prev_page,
    }


# Get a single item by its ID
def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

# Update an existing item in the database
def update_item(db: Session, item_id: int, name: str, description: str,price: float, category: str, photo:str):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db_item.name = name
        db_item.description = description
        db_item.price = price
        db_item.category = category
        db_item.photo = photo
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

# Seeder function to insert 100+ product data with photos
def seed_data(db: Session):
    fake = Faker()
    items = []

    # Example categories
    categories = ["Electronics", "Home Appliances", "Furniture", "Clothing", "Toys", "Books", "Sports", "Beauty"]

    # Generate 100+ fake product items
    for _ in range(100):
        item = Item(
            name=fake.unique.word().capitalize() + " " + random.choice(["Pro", "Plus", "Lite", "Max"]),
            description=fake.text(max_nb_chars=200),  # Product description
            price=round(random.uniform(10.0, 1000.0), 2),  # Random price between $10 and $1000
            category=random.choice(categories),  # Randomly assign a category
            photo=f"https://picsum.photos/seed/{fake.uuid4()}/200/300"  # Random photo URL from Lorem Picsum
        )
        items.append(item)

    # Add all items to the session
    db.add_all(items)
    db.commit()

    return {"message": f"Seeded {len(items)} product items successfully!"}

def clear_all_data(db: Session):
    try:
        # Clear data from each table
        db.query(Item).delete()  # Add other tables here if necessary
        db.commit()
        return {"message": "All data cleared successfully!"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}