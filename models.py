from sqlalchemy import Column, Integer, String,Float
from database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    photo = Column(String(255), nullable=True)  # New field for photo
