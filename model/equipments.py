from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db
import datetime
import logging
from typing import List,Optional, Dict, Union
import json

logger = logging.getLogger(__name__)
equipments = APIRouter(tags=["For Equipments"])

@equipments.post("/equipment/add", response_model=dict)
async def add_equipments(
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
        return {"item_ID": find_item[0], "item_name": find_item[1],  "quantity": find_item[2],"status": find_item[3]}
    raise HTTPException(status_code=404, detail="User not found")




@equipments.put("/equipment/edit/{equipment_id}", response_model=dict)
async def edit_equipment(
    equipment_id: int,
    item_name: str = Form(...),
    quantity: int = Form(...), 
    status: str = Form(...), 
    db=Depends(get_db)
):
    try:
        # Update the equipment based on the received item name
        query_update_equipment = "UPDATE equipments SET item_name = %s, quantity = %s, status = %s WHERE item_id = %s"
        db[0].execute(query_update_equipment, (item_name, quantity, status, equipment_id))
        db[1].commit()

        # Check if the quantity is zero and update the status accordingly
        if quantity == 0:
            query_update_status = "UPDATE equipments SET status = 'Not Available' WHERE item_id = %s"
            db[0].execute(query_update_status, (equipment_id,))
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
    
    
    
from typing import List, Dict, Union, Optional
from fastapi import HTTPException, Depends
import datetime

@equipments.post("/equipment/request", response_model=dict)
async def request_equipment(
    request_data: dict,  # Updated to accept a dictionary containing request data
    db=Depends(get_db)
):
    try:
        # Extract request data
        user_id = request_data.get("user_id")
        user_name = request_data.get("user_name")
        user_type = request_data.get("user_type")
        year_section = request_data.get("year_section")
        item_requests = request_data.get("item_requests")

        if not all([user_id, user_name, user_type, item_requests]):
            raise HTTPException(status_code=400, detail="Missing required fields in the request")

        requested_item_names = []  # List to store requested item names
        requested_item_ids = []  # List to store requested item IDs
        requested_item_quantities = []  # List to store requested item quantities

        # Process item requests and aggregate item names, IDs, and quantities
        for item_request in item_requests:
            item_id = item_request.get("item_id")
            quantity = item_request.get("quantity")

            if item_id is None or quantity is None:
                raise HTTPException(status_code=400, detail="Item ID or quantity is missing in one or more requests")

            # Fetch the item_name based on the item_id
            query_fetch_item_name = "SELECT item_name FROM equipments WHERE item_id = %s"
            db[0].execute(query_fetch_item_name, (item_id,))
            item_name = db[0].fetchone()

            if not item_name:
                raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")

            requested_item_ids.append(item_id)  # Add item ID to the list
            requested_item_names.append(item_name[0])  # Add item name to the list
            requested_item_quantities.append(quantity)  # Add item quantity to the list

        # Serialize lists into comma-separated strings
        concatenated_item_ids = ', '.join(map(str, requested_item_ids))
        concatenated_item_names = ', '.join(requested_item_names)
        concatenated_item_quantities = ', '.join(map(str, requested_item_quantities))

        # Insert user-specific data into the respective tables
        if user_type == "student":
            query_insert_student = "INSERT INTO student (student_id, student_name, year_section) VALUES (%s, %s, %s)"
            db[0].execute(query_insert_student, (user_id, user_name, year_section))
            db[1].commit()
        elif user_type == "teacher":
            query_insert_teacher = "INSERT INTO teacher (teacher_id, teacher_name) VALUES (%s, %s)"
            db[0].execute(query_insert_teacher, (user_id, user_name))
            db[1].commit()
        elif user_type == "personnel":
            query_insert_personnel = "INSERT INTO personnel (personnel_id, personnel_name) VALUES (%s, %s)"
            db[0].execute(query_insert_personnel, (user_id, user_name))
            db[1].commit()

        # Insert the aggregated item IDs, names, and quantities into the request table
        timestamp = datetime.datetime.now()
        query_insert_request = """
            INSERT INTO request 
            (user_id, name, date, year_section, item_id, item_name, quantity, user_type) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        db[0].execute(query_insert_request, (
            user_id, user_name, timestamp, year_section,
            concatenated_item_ids, concatenated_item_names, concatenated_item_quantities,
            user_type
        ))
        db[1].commit()

        return {"message": "Equipment request(s) submitted successfully", "requested_item_names": concatenated_item_names, "Concat Names": concatenated_item_quantities, "Concat_ID": concatenated_item_ids}
    except HTTPException as http_exception:
        raise http_exception  # Re-raise HTTPException to maintain its original status code and detail
    except Exception as e:
        logger.exception("An error occurred while processing equipment request:")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        db[0].close()




