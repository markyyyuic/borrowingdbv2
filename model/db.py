# model/db.py
import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "entdb",
    "port": 3306,
}

def get_db():
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        yield cursor, db
    finally:
        cursor.close()
        db.close()
        
def fetch_admin_id_from_database() -> int:
    """
    Fetches the admin ID from the database based on the context of the current session or request.
    Returns the admin ID if found, otherwise returns None.
    """
    # Implement your logic here to fetch the admin ID based on the context of the current session or request
    # This might involve accessing session data, token authentication, or other context-specific information
    
    # For now, return a placeholder value (e.g., 1)
    return 1
