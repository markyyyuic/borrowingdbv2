from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db
import datetime
import logging

logger = logging.getLogger(__name__)
equipments = APIRouter(tags=["For Equipments"])

@equipments.post("/equipment/add", response_model=dict)
async def add_equipment(
    item_name: str = Form(...),
    quantity: int = Form(...), 
    status: str = Form(...), 
    db=Depends(get_db)
):
    try:
        # Insert the equipment into the equipment table
        query_add_equipment = "INSERT INTO equipments (item_name, quantity, status) VALUES (%s, %s, %s)"
        db[0].execute(query_add_equipment, (item_name, quantity, status))
        
        # Retrieve the last inserted ID using LAST_INSERT_ID()
        db[0].execute("SELECT LAST_INSERT_ID()")
        new_equipment_id = db[0].fetchone()[0]
        
        db[1].commit()  # Commit the transaction
        
        return {"item_name": item_name, "quantity": quantity, "status": status, "equipment_id": new_equipment_id}
    except Exception as e:
        logger.exception("Error occurred while adding equipment:")
        raise HTTPException(status_code=500, detail="Internal server error")
    
    

@equipments.get("/equipments/equipment_list", response_model=list)
async def get_equipmentlist(
    db=Depends(get_db)
):
    query = "SELECT item_id, item_name, quantity, status, status FROM equipments"
    db[0].execute(query)
    items = [{"item_id": items[0], "item_name": items[1], "quantity": items[2], "status": items[3]} for items in db[0].fetchall()]
    return items

@equipments.get("/equipment/find_equipment", response_model=dict)
async def find_equipment(
    item_id: int, 
    db=Depends(get_db)
):
    query = "SELECT item_id, item_name, quantity, status from equipments WHERE item_ID = %s"
    db[0].execute(query, ( item_id,))
    find_item = db[0].fetchone()
    if find_item:
        return {"item_ID": find_item[0], "item_name": find_item[1],  "quantity": find_item[2],"status": user[3]}
    raise HTTPException(status_code=404, detail="User not found")

@equipments.post("/equipment/add", response_model=dict)
async def add_equipment(
    item_name: str = Form(...),
    quantity: int = Form(...), 
    status: str = Form(...), 
    db=Depends(get_db)
):
    try:
        # Insert the equipment into the equipment table
        query_add_equipment = "INSERT INTO equipments (item_name, quantity, status) VALUES (%s, %s, %s)"
        db[0].execute(query_add_equipment, (item_name, quantity, status))
        
        # Retrieve the last inserted ID using LAST_INSERT_ID()
        db[0].execute("SELECT LAST_INSERT_ID()")
        new_equipment_id = db[0].fetchone()[0]
        
        db[1].commit()  # Commit the transaction
        
        return {"item_name": item_name, "quantity": quantity, "status": status, "equipment_id": new_equipment_id}
    except Exception as e:
        logger.exception("Error occurred while adding equipment:")
        raise HTTPException(status_code=500, detail="Internal server error")


@equipments.put("/equipment/edit/{equipment_id}", response_model=dict)
async def edit_equipment(
    equipment_id: int,
    item_name: str = Form(...),
    quantity: int = Form(...), 
    status: str = Form(...), 
    db=Depends(get_db)
):
    try:
        # Check if the equipment exists
        query_check_equipment = "SELECT item_id FROM equipments WHERE item_id = %s"
        db[0].execute(query_check_equipment, (equipment_id,))
        existing_equipment = db[0].fetchone()

        if not existing_equipment:
            raise HTTPException(status_code=404, detail="Equipment not found")

        # Update the equipment
        query_update_equipment = "UPDATE equipments SET item_name = %s, quantity = %s, status = %s WHERE item_id = %s"
        db[0].execute(query_update_equipment, (item_name, quantity, status, equipment_id))
        db[1].commit()

        return {"message": "Equipment updated successfully"}
    except Exception as e:
        logger.exception("Error occurred while updating equipment:")
        raise HTTPException(status_code=500, detail="Internal server error")

@equipments.delete("/equipment/delete/{equipment_id}", response_model=dict)
async def delete_equipment(
    equipment_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the equipment exists
        query_check_equipment = "SELECT item_id FROM equipments WHERE item_id = %s"
        db[0].execute(query_check_equipment, (equipment_id,))
        existing_equipment = db[0].fetchone()

        if not existing_equipment:
            raise HTTPException(status_code=404, detail="Equipment not found")

        # Delete the equipment
        query_delete_equipment = "DELETE FROM equipments WHERE item_id = %s"
        db[0].execute(query_delete_equipment, (equipment_id,))
        db[1].commit()

        return {"message": "Equipment deleted successfully"}
    except Exception as e:
        logger.exception("Error occurred while deleting equipment:")
        raise HTTPException(status_code=500, detail="Internal server error")
    
    
    
@equipments.post("/equipment/request", response_model=dict)
async def request_equipment(
    user_id: int, 
    item_id: int,
    user_type: str,
    db=Depends(get_db)
):
    try:
        # Check if the user exists based on the user_type
        if user_type == "student":
            query_check_user = "SELECT student_id FROM student WHERE student_id = %s"
        elif user_type == "teacher":
            query_check_user = "SELECT Teacher_ID FROM teacher WHERE Teacher_ID = %s"
        elif user_type == "personnel":
            query_check_user = "SELECT personnel_id FROM personnel WHERE personnel_id = %s"
        else:
            raise HTTPException(status_code=400, detail="Invalid user type")

        db[0].execute(query_check_user, (user_id,))
        existing_user = db[0].fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail=f"{user_type.capitalize()} not found")

        # Fetch the item_name based on the item_id
        query_fetch_item_name = "SELECT item_name FROM equipments WHERE item_id = %s"
        db[0].execute(query_fetch_item_name, (item_id,))
        item_name = db[0].fetchone()

        if not item_name:
            raise HTTPException(status_code=404, detail="Item not found")

        # Insert the request into the request table
        timestamp = datetime.datetime.now()
        if user_type == "student":
            query_insert_request = "INSERT INTO request (student_id, date, item_id, item_name) VALUES (%s, %s, %s, %s)"
        elif user_type == "teacher":
            query_insert_request = "INSERT INTO request (teacher_id, date, item_id, item_name) VALUES (%s, %s, %s, %s)"
        elif user_type == "personnel":
            query_insert_request = "INSERT INTO request (personnel_id, date, item_id, item_name) VALUES (%s, %s, %s, %s)"
        
        db[0].execute(query_insert_request, (user_id, timestamp, item_id, item_name[0]))
        db[1].commit()

        return {"message": "Equipment request submitted successfully"}
    except Exception as e:
        logger.exception("An error occurred while processing equipment request:")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()
