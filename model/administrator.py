from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db, hash_password, fetch_admin_id_from_database
from typing import Dict
from sqlalchemy import text  # Import text from sqlalchemy
import bcrypt

administrator = APIRouter(tags=["Administrator Panel"])

# CRUD operations

@administrator.post("/administrator/login/", response_model=Dict)
async def login_administrator(username: str = Form(...), password: str = Form(...), db=Depends(get_db)):
    query_check_user = text("SELECT admin_id, username, password FROM administrator WHERE username = :username")
    user = db.execute(query_check_user, {"username": username}).fetchone()

    if user:
        stored_hashed_password = user[2]
        admin_id = user[0]

        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            print(f"Admin logged in: username - {username}, admin_id - {admin_id}")
            return {"message": "Login successful", "admin_id": admin_id, "username": username}

    raise HTTPException(status_code=401, detail="Incorrect username or password")



@administrator.get("/administrator/account_list", response_model=list)
async def admin_list(db=Depends(get_db)):
    query = text("SELECT admin_id, username, full_name FROM administrator")
    users = [{"admin_id": user[0], "username": user[1], "full_name": user[2]} for user in db.execute(query).fetchall()]
    return users





@administrator.get("/administrator/get_admin_account", response_model=dict)
async def find_admin(admin_id: int, db=Depends(get_db)):
    query = text("SELECT admin_id, username, full_name FROM administrator WHERE admin_id = :admin_id")
    user = db.execute(query, {"admin_id": admin_id}).fetchone()
    if user:
        return {"admin_id": user[0], "username": user[1], "full_name": user[2]}
    raise HTTPException(status_code=404, detail="User not found")



#Creating 
@administrator.post("/administrator/create", response_model=dict)
async def create_administrator(username: str = Form(...), password: str = Form(...), full_name: str = Form(...), db=Depends(get_db)):
    
    #make the password hashed
    hashed_password = hash_password(password)
    #query to inset the account into administrator table
    query = text("INSERT INTO administrator (username, password, full_name) VALUES (:username, :password, :full_name)")
    
    #executes the query in database
    db.execute(query, {"username": username, "password": hashed_password, "full_name": full_name})
    #then Commits 
    db.commit()
    return {"message": "Admin account created successfully"}




@administrator.put("/administrator/edit/", response_model=dict)
async def update_administrator(admin_id: int, username: str = Form(...), password: str = Form(...), full_name: str = Form(...), db=Depends(get_db)):
    hashed_password = hash_password(password)
    query = text("UPDATE administrator SET username = :username, password = :password, full_name = :full_name WHERE admin_id = :admin_id")
    db.execute(query, {"username": username, "password": hashed_password, "full_name": full_name, "admin_id": admin_id})
    db.commit()
    return {"message": "Admin account updated successfully"}




@administrator.delete("/administrator/delete/", response_model=dict)
async def delete_administrator(admin_id: int, db=Depends(get_db)):
    query = text("DELETE FROM administrator WHERE admin_id = :admin_id")
    db.execute(query, {"admin_id": admin_id})
    db.commit()
    return {"message": "Admin account deleted successfully"}




@administrator.post("/admin/equipment/create", response_model=dict)
async def create_equipment_by_admin(
    item_name: str = Form(...), 
    quantity: int = Form(...), 
    status: str = Form(...), 
    admin_id: int = Depends(fetch_admin_id_from_database),  # Fetch admin_id directly
    db=Depends(get_db)
) -> Dict:
    # Check if all required fields are provided
    if not all((item_name, quantity, status)):
        raise HTTPException(status_code=400, detail="All fields are required")
    
    # Insert the new equipment item into the database
    query = text("""
        INSERT INTO equipments (item_name, quantity, status, admin_id)
        VALUES (:item_name, :quantity, :status, :admin_id)
    """)
    db.execute(query, {"item_name": item_name, "quantity": quantity, "status": status, "admin_id": admin_id})
    db.commit()
    
    return {"message": "Equipment added successfully by administrator"}





# Endpoint to update an existing equipment item by administrator
@administrator.put("/admin/equipment/edit/{item_id}", response_model=dict)
async def update_equipment_by_admin(
    item_id: int,
    item_name: str = Form(...),
    quantity: int = Form(...),
    status: str = Form(...),
    admin_id: int = Depends(fetch_admin_id_from_database),
    db=Depends(get_db)
):
    # Check if the equipment item exists
    query_check_item = text("SELECT * FROM equipments WHERE item_id = :item_id")
    existing_item = db.execute(query_check_item, {"item_id": item_id}).fetchone()
    if not existing_item:
        raise HTTPException(status_code=404, detail="Equipment item not found")

    # Fetch the full name of the administrator
    query_get_admin_name = text("SELECT full_name FROM administrator WHERE admin_id = :admin_id")
    admin_name = db.execute(query_get_admin_name, {"admin_id": admin_id}).fetchone()[0]

    # Fetch the current latest editor and update it as last editor
    query_get_latest_editor = text("SELECT latest_editor FROM equipments WHERE item_id = :item_id")
    current_latest_editor = db.execute(query_get_latest_editor, {"item_id": item_id}).fetchone()[0]

    # Update the existing equipment item in the database
    query_update_item = text("""
        UPDATE equipments 
        SET item_name = :item_name, quantity = :quantity, status = :status, last_editor_id = :admin_id, latest_editor = :admin_name, last_editor = :current_latest_editor
        WHERE item_id = :item_id
    """)
    db.execute(query_update_item, {
        "item_name": item_name,
        "quantity": quantity,
        "status": status,
        "admin_id": admin_id,
        "admin_name": admin_name,
        "current_latest_editor": current_latest_editor,
        "item_id": item_id
    })
    db.commit()

    # Check if the quantity is greater than 0 and update the status accordingly
    if quantity > 0:
        query_update_status = text("""
            UPDATE equipments
            SET status = 'Available'
            WHERE item_id = :item_id
        """)
        db.execute(query_update_status, {"item_id": item_id})
        db.commit()

    return {"message": "Equipment updated successfully by administrator"}





@administrator.delete("/admin/equipment/delete/{item_id}", response_model=dict)
async def delete_equipment_by_admin(
    item_id: int,
    username: str,  # Add username as a parameter
    db=Depends(get_db)
):
    admin_id = fetch_admin_id_from_database(username=username)  # Pass username as an argument  
    if admin_id is None:
        raise HTTPException(status_code=500, detail="Failed to fetch admin ID")

    # Ensure that the admin requesting the deletion has the necessary permissions

    # Check if the equipment item exists
    query_check_item = text("SELECT * FROM equipments WHERE item_id = :item_id")
    existing_item = db.execute(query_check_item, {"item_id": item_id}).fetchone()
    if not existing_item:
        raise HTTPException(status_code=404, detail="Equipment item not found")

    # Disable foreign key checks
    query_disable_foreign_key_checks = text("SET foreign_key_checks = 0")
    db.execute(query_disable_foreign_key_checks)

    try:
        # Perform the deletion operation
        query_delete_item = text("DELETE FROM equipments WHERE item_id = :item_id")
        db.execute(query_delete_item, {"item_id": item_id})
        db.commit()
    finally:
        # Enable foreign key checks
        query_enable_foreign_key_checks = text("SET foreign_key_checks = 1")
        db.execute(query_enable_foreign_key_checks)

    return {"message": "Equipment deleted successfully by administrator"}


   
