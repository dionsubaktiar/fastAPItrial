from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL connection string (replace with your actual database credentials)
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://u1248453_nusantara:Marlboro39.@nusantaratranssentosa.co.id:3306/u1248453_fastapi"

# Create the SQLAlchemy engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
