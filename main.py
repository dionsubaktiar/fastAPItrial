from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import crud, models
from crud import clear_all_data,seed_data

# Create the tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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
@app.post("/items/")
def create_item(name: str, description: str, db: Session = Depends(get_db)):
    return crud.create_item(db=db, name=name, description=description)

# Read Item by ID (GET)
@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# Read all Items (GET)
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_items(db=db, skip=skip, limit=limit)

# Update Item (PUT)
@app.put("/items/{item_id}")
def update_item(item_id: int, name: str, description: str, db: Session = Depends(get_db)):
    db_item = crud.update_item(db=db, item_id=item_id, name=name, description=description)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

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

