# model/users.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db
import bcrypt
from typing import Dict
from fastapi import Depends
from .db import fetch_admin_id_from_database


administrator = APIRouter(tags=["Administrator Panel"])

# CRUD operations

# Endpoint to handle administrator login
@administrator.post("/administrator/login/", response_model=dict)
async def login_administrator(
    username: str = Form(...), 
    password: str = Form(...), 
    db=Depends(get_db)
):
    # Query the database to check if the username exists
    query_check_user = "SELECT admin_id, password FROM administrator WHERE username = %s"
    db[0].execute(query_check_user, (username,))
    user = db[0].fetchone()

    if user:
        # Retrieve the stored password and admin_id from the database
        stored_password = user[1]
        admin_id = user[0]

        # Check if the password is correct
        if password == stored_password:
            # If username and password are correct, return login successful along with admin_id
            return {"message": "Login successful", "admin_id": admin_id}
    
    # If username or password is incorrect, raise an HTTPException
    raise HTTPException(status_code=401, detail="Incorrect username or password")






@administrator.get("/administrator/account_list", response_model=list)
async def admin_list(
    db=Depends(get_db)
):
    query = "SELECT admin_id, username, password FROM administrator"
    db[0].execute(query)
    users = [{"admin_id": user[0], "username": user[1], "password": user[2]} for user in db[0].fetchall()]
    return users

@administrator.get("/administrator/get_admin_account", response_model=dict)
async def find_admin(
    admin_id: int,
    db=Depends(get_db)
):
    query = "SELECT admin_id, username, password FROM administrator WHERE admin_id = %s"
    db[0].execute(query, (admin_id,))
    user = db[0].fetchone()
    if user:
        return {"admin_id": user[0], "username": user[1], "password": user[2]}
    raise HTTPException(status_code=404, detail="User not found")

@administrator.post("/administrator/create", response_model=dict)
async def create_administrator(
    username: str = Form(...), 
    password: str = Form(...), 
    db=Depends(get_db)
) -> Dict:

    query = "INSERT INTO administrator (username, password) VALUES (%s, %s)"
    db[0].execute(query, (username, password))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_user_id = db[0].fetchone()[0]
    db[1].commit()
    
    return {"admin_id": new_user_id, "username": username, "password": password, "message": "Admin account was created successfully"}

@administrator.put("/administrator/edit/", response_model=dict)
async def update_administrator(
    admin_id: int,
    username: str = Form(...),
    password: str = Form(None),  # Allow password to be optional
    db=Depends(get_db)
):
    # Check if password is provided and hash it if necessary
    if password:
        hashed_password = hash_password(password)
    else:
        # If password is not provided, fetch the existing hashed password from the database
        query_get_password = "SELECT password FROM administrator WHERE admin_id = %s"
        db[0].execute(query_get_password, (admin_id,))
        existing_password = db[0].fetchone()
        if existing_password:
            hashed_password = existing_password[0]
        else:
            raise HTTPException(status_code=404, detail="User not found")

    # Update user information in the database
    query = "UPDATE administrator SET username = %s, admin_Password = %s WHERE admin_id = %s"
    db[0].execute(query, (username, hashed_password, admin_id))
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "User updated successfully"}
    raise HTTPException(status_code=404, detail="User not found")


@administrator.delete("/administrator/delete/", response_model=dict)
async def delete_administrator(
    adminID: int,
    db=Depends(get_db)
):
    try:
        # Disable foreign key checks
        db[0].execute("SET foreign_key_checks = 0")
        db[1].commit()

        # Check if the user exists
        query_check_user = "SELECT admin_id FROM administrator WHERE admin_id = %s"
        db[0].execute(query_check_user, (adminID,))
        existing_user = db[0].fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Delete the user
        query_delete_user = "DELETE FROM administrator WHERE admin_id = %s"
        db[0].execute(query_delete_user, (adminID,))
        db[1].commit()

        # Re-enable foreign key checks
        db[0].execute("SET foreign_key_checks = 1")
        db[1].commit()

        return {"message": "Admin deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()






# FOR ADD, EDIT, DELETE equipments methods

# Endpoint to create a new equipment item by administrator
@administrator.post("/admin/equipment/create", response_model=dict)
async def create_equipment_by_admin(
    item_name: str = Form(...), 
    quantity: int = Form(...), 
    status: str = Form(...), 
    db=Depends(get_db)
) -> Dict:
    # Check if all required fields are provided
    if not all((item_name, quantity, status)):
        raise HTTPException(status_code=400, detail="All fields are required")
    
    # Fetch the admin ID directly from the database
    admin_id = fetch_admin_id_from_database()  
    if admin_id is None:
        raise HTTPException(status_code=500, detail="Failed to fetch admin ID")

    # Insert the new equipment item into the database
    query = "INSERT INTO equipments (item_name, quantity, status, admin_id, last_editor_id) VALUES (%s, %s, %s, %s, %s)"
    db[0].execute(query, (item_name, quantity, status, admin_id, admin_id))
    db[1].commit()
    
    return {"message": "Equipment added successfully by administrator"}


# Endpoint to update an existing equipment item by administrator
@administrator.put("/admin/equipment/edit/{item_id}", response_model=dict)
async def update_equipment_by_admin(
    item_id: int,
    item_name: str = Form(...),
    quantity: int = Form(...),
    status: str = Form(...),
    db=Depends(get_db)
):
    # Fetch the admin ID directly from the database
    admin_id = fetch_admin_id_from_database()  
    if admin_id is None:
        raise HTTPException(status_code=500, detail="Failed to fetch admin ID")

    # Check if the equipment item exists
    query_check_item = "SELECT * FROM equipments WHERE item_id = %s"
    db[0].execute(query_check_item, (item_id,))
    existing_item = db[0].fetchone()
    if not existing_item:
        raise HTTPException(status_code=404, detail="Equipment item not found")

    # Update the existing equipment item in the database
    query_update_item = "UPDATE equipments SET item_name = %s, quantity = %s, status = %s, last_editor_id = %s WHERE item_id = %s"
    db[0].execute(query_update_item, (item_name, quantity, status, admin_id, item_id))
    db[1].commit()
    
    return {"message": "Equipment updated successfully by administrator"}


# Endpoint to delete an existing equipment item by administrator
@administrator.delete("/admin/equipment/delete/{item_id}", response_model=dict)
async def delete_equipment_by_admin(
    item_id: int,
    db=Depends(get_db)
):
    # Fetch the admin ID directly from the database
    admin_id = fetch_admin_id_from_database()  
    if admin_id is None:
        raise HTTPException(status_code=500, detail="Failed to fetch admin ID")

    # Delete the existing equipment item from the database
    query_delete_item = "DELETE FROM equipments WHERE item_id = %s"
    db[0].execute(query_delete_item, (item_id,))
    db[1].commit()
    
    return {"message": "Equipment deleted successfully by administrator"}



# Endpoint to delete an existing equipment entry by administrator
@administrator.delete("/admin/equipment/delete/{item_id}", response_model=dict)
async def delete_equipment_by_admin(
    item_id: int,
    db=Depends(get_db)
):
    # Fetch the admin ID directly from the database (replace 'admin_id' with your actual column name)
    admin_id = fetch_admin_id_from_database()  # Implement this function to fetch admin ID
    if admin_id is None:
        raise HTTPException(status_code=500, detail="Failed to fetch admin ID")

    # Delete the existing equipment entry from the database
    query = "DELETE FROM equipments WHERE item_id = %s AND admin_id = %s"
    db[0].execute(query, (item_id, admin_id))
    db[1].commit()
    
    return {"message": "Equipment deleted successfully by administrator"}