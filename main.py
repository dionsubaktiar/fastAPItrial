import os
import shutil
from fastapi import FastAPI, Depends, HTTPException, Query, Request, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import crud, models
from crud import UPLOAD_DIRECTORY, clear_all_data,seed_data, get_items, create_item

# Create the tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Mount the static files directory
app.mount("/uploaded_images", StaticFiles(directory=UPLOAD_DIRECTORY), name="uploaded_images")

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"Hello": "World"}

# Create Item (POST)
# Create Item (POST)
@app.post("/items/")
async def add_item(
    request: Request, 
    name: str = Form(...),  # Form field for name
    description: str = Form(...),  # Form field for description
    price: float = Form(...),  # Form field for price
    category: str = Form(...),  # Form field for category
    photo: UploadFile = File(...),  # File field for photo
    db: Session = Depends(get_db),  # Database session dependency
):
    try:
        # Save the uploaded photo
        file_location = os.path.join(UPLOAD_DIRECTORY, photo.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

        # Generate the public URL for the uploaded photo
        public_photo_url = f"{request.base_url}uploaded_images/{photo.filename}"

        # Call the CRUD function to create the item in the database
        new_item = create_item(
            db=db,
            name=name,
            description=description,
            price=price,
            category=category,
            photo=public_photo_url,  # Save the public URL in the database
        )

        return {
            "message": "Item created successfully",
            "item": {
                "id": new_item.id,
                "name": new_item.name,
                "description": new_item.description,
                "price": new_item.price,
                "category": new_item.category,
                "photo": new_item.photo,  # Return the public URL
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Read Item by ID (GET)
@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.get("/items/")
def fetch_items(
    request: Request,  # Add request parameter
    page: int = Query(1, ge=1),  # Page number must be >= 1
    page_size: int = Query(10, le=100),  # Page size must be <= 100
    db: Session = Depends(get_db),
):
    """
    Fetch paginated list of items.
    """
    result = get_items(db, request=request, page=page, page_size=page_size)
    return result

# Update Item (PUT)
@app.put("/items/{item_id}")
async def update_item(
    request:Request,
    item_id: int,
    name: str = Form(None),  # Optional name field
    description: str = Form(None),  # Optional description field
    price: float = Form(None),  # Optional price field
    category: str = Form(None),  # Optional category field
    photo: UploadFile = File(None),  # Optional photo field
    db: Session = Depends(get_db),  # Database session
):
    # Fetch the item from the database
    db_item = crud.get_item(db=db, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Update fields if they are provided
    if name:
        db_item.name = name
    if description:
        db_item.description = description
    if price is not None:
        db_item.price = price
    if category:
        db_item.category = category

    # Handle photo upload if provided
    if photo:
        try:
            # Save the uploaded photo
            file_location = os.path.join(UPLOAD_DIRECTORY, photo.filename)
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(photo.file, buffer)
            # Update the photo field
            db_item.photo = f"{request.base_url}uploaded_images/{photo.filename}"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Photo upload failed: {str(e)}")

    # Commit the updates to the database
    db.commit()
    db.refresh(db_item)

    return {
        "message": "Item updated successfully",
        "item": {
            "id": db_item.id,
            "name": db_item.name,
            "description": db_item.description,
            "price": db_item.price,
            "category": db_item.category,
            "photo": db_item.photo,
        },
    }


# Delete Item (DELETE)
@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.post("/seed/")
def run_seeder(db: Session = Depends(get_db)):
    result = seed_data(db)
    return result

@app.post("/clear/")
def clear_data(db: Session = Depends(get_db)):
    result = clear_all_data(db)
    return result

