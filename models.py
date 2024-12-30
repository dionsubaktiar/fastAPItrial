from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Create the base class for models
Base = declarative_base()

# Define the Item model
class Item(Base):
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))

# Create the database connection
engine = create_engine('mysql+mysqlconnector://u1248453_nusantara:Marlboro39.@nusantaratranssentosa.co.id:3306/u1248453_fastapi')
Session = sessionmaker(bind=engine)
session = Session()
