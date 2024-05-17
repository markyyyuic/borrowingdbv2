import mysql.connector
import bcrypt
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Define SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:@localhost/entdb"

# Create database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a Session class bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to get a database session
def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()

# Database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",  # Update with your actual password
    "database": "entdb",
    "port": 3306,
}

def fetch_admin_id_from_database(username: str) -> int:
    query = "SELECT admin_id FROM administrator WHERE username = %s"
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(query, (username,))
    admin_id = cursor.fetchone()
    cursor.close()
    db.close()
    if admin_id:
        return admin_id[0]
    else:
        return None

def hash_password(password: str) -> str:
    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')
