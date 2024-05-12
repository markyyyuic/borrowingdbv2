from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


SQLALCHEMY_DATABASE_URL = "mysql+pymysql://sql6705923:<password>@sql6.freemysqlhosting.net:3306/sql6705923"


# Create a SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create a sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define your database models using SQLAlchemy's ORM
# Example:
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

# Define your fetch_admin_id_from_database function
def fetch_admin_id_from_database(db):
    """
    Fetches the admin ID from the database based on the context of the current session or request.
    Returns the admin ID if found, otherwise returns None.
    """
    try:
        # Implement your logic here to fetch the admin ID based on the context of the current session or request
        # This might involve executing a SQL query using SQLAlchemy
        
        # For now, return a placeholder value (e.g., 1)
        # Replace this with your actual logic to fetch the admin ID
        admin_id = 1
        
        return admin_id
    except SQLAlchemyError as e:
        # Handle any database errors gracefully
        print(f"Error fetching admin ID: {e}")
        return None
