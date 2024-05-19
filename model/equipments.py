from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db
import datetime
import logging
from typing import List, Optional, Dict, Union
import json
from sqlalchemy.exc import SQLAlchemyError
from .models import Equipment, Student, Teacher, Personnel, Request as RequestModel 
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy import desc
from fastapi.responses import JSONResponse
import base64
from model import crud
from sqlalchemy.exc import IntegrityError
from datetime import date
from sqlalchemy import text


logger = logging.getLogger(__name__)
equipments = APIRouter(tags=["For Equipments"])

@equipments.post("/equipment/add", response_model=dict)
async def add_equipments(
    item_name: str = Form(...),
    quantity: int = Form(...), 
    status: str = Form(...), 
    db=Depends(get_db)
):
    cursor, conn = db
    try:
        # Insert the equipment into the equipment table
        query_add_equipment = "INSERT INTO equipments (item_name, quantity, status) VALUES (%s, %s, %s)"
        cursor.execute(query_add_equipment, (item_name, quantity, status))
        
        # Retrieve the last inserted ID using LAST_INSERT_ID()
        cursor.execute("SELECT LAST_INSERT_ID()")
        new_equipment_id = cursor.fetchone()[0]
        
        conn.commit()  # Commit the transaction
        
        return {"item_name": item_name, "quantity": quantity, "status": status, "equipment_id": new_equipment_id}
    except Exception as e:
        logger.exception("Error occurred while adding equipment:")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        cursor.close()
        conn.close()

from fastapi.responses import JSONResponse

@equipments.get("/equipments/equipment_list", response_model=list)
async def get_equipmentlist(
    db: Session = Depends(get_db)
):
    try:
        with db as session:
            # Fetch all equipments using SQLAlchemy query
            equipments = session.query(Equipment).all()
            # Convert SQLAlchemy objects to dictionaries
            equipment_list = [
                {
                    "item_id": equipment.item_id,
                    "item_name": equipment.item_name,
                    "quantity": equipment.quantity,
                    "status": equipment.status,
                    # Convert image to base64 string for display
                   "image": base64.b64encode(equipment.image).decode("utf-8") if equipment.image else None
                }
                for equipment in equipments
            ]
            return equipment_list
    except SQLAlchemyError as e:
        logger.exception("Error occurred while retrieving equipment list:")
        raise HTTPException(status_code=500, detail="Internal server error")




@equipments.get("/equipment/find_equipment", response_model=dict)
async def find_equipment(
    item_id: int, 
    db=Depends(get_db)
):
    cursor, conn = db
    try:
        query = "SELECT item_id, item_name, quantity, status FROM equipments WHERE item_id = %s"
        cursor.execute(query, (item_id,))
        find_item = cursor.fetchone()
        if find_item:
            return {"item_id": find_item[0], "item_name": find_item[1],  "quantity": find_item[2], "status": find_item[3]}
        raise HTTPException(status_code=404, detail="Equipment not found")
    except Exception as e:
        logger.exception("Error occurred while finding equipment:")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        cursor.close()
        conn.close()

@equipments.put("/equipment/edit/{equipment_id}", response_model=dict)
async def edit_equipment(
    equipment_id: int,
    item_name: str = Form(...),
    quantity: int = Form(...), 
    status: str = Form(...), 
    db=Depends(get_db)
):
    cursor, conn = db
    try:
        # Update the equipment based on the received item name
        query_update_equipment = "UPDATE equipments SET item_name = %s, quantity = %s, status = %s WHERE item_id = %s"
        cursor.execute(query_update_equipment, (item_name, quantity, status, equipment_id))
        conn.commit()

        # Check if the quantity is zero and update the status accordingly
        if quantity == 0:
            query_update_status = "UPDATE equipments SET status = 'Not Available' WHERE item_id = %s"
            cursor.execute(query_update_status, (equipment_id,))
            conn.commit()

        return {"message": "Equipment updated successfully"}
    except Exception as e:
        logger.exception("Error occurred while updating equipment:")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        cursor.close()
        conn.close()

@equipments.delete("/equipment/delete/{equipment_id}", response_model=dict)
async def delete_equipment(
    equipment_id: int,
    db=Depends(get_db)
):
    cursor, conn = db
    try:
        # Check if the equipment exists
        query_check_equipment = "SELECT item_id FROM equipments WHERE item_id = %s"
        cursor.execute(query_check_equipment, (equipment_id,))
        existing_equipment = cursor.fetchone()

        if not existing_equipment:
            raise HTTPException(status_code=404, detail="Equipment not found")

        # Delete the equipment
        query_delete_equipment = "DELETE FROM equipments WHERE item_id = %s"
        cursor.execute(query_delete_equipment, (equipment_id,))
        conn.commit()

        return {"message": "Equipment deleted successfully"}
    except Exception as e:
        logger.exception("Error occurred while deleting equipment:")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        cursor.close()
        conn.close()
        
        
@equipments.post("/equipment/request", response_model=dict)
async def request_equipment(
    request_data: dict,  # Changed parameter to accept JSON data
    db: Session = Depends(get_db)
):
    try:
        user_id = request_data.get("user_id")
        user_name = request_data.get("user_name")
        user_type = request_data.get("user_type")
        year_section = request_data.get("year_section")
        item_requests = request_data.get("item_requests")

        # Check if item_requests is empty
        if not item_requests:
            raise HTTPException(status_code=400, detail="Item requests cannot be empty")

        requested_item_names = []
        requested_item_ids = []
        requested_item_quantities = []

        # Iterate over item requests
        for item_request in item_requests:
            item_id = item_request.get("item_id")
            quantity = item_request.get("quantity")
            if item_id is None or quantity is None:
                raise HTTPException(status_code=400, detail="Item ID or quantity is missing in one or more requests")

            # Check if the item with item_id exists in the database
            item = db.query(Equipment).filter(Equipment.item_id == item_id).first()
            if not item:
                raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")

            requested_item_ids.append(item_id)
            requested_item_names.append(item.item_name)
            requested_item_quantities.append(quantity)

        concatenated_item_ids = ', '.join(map(str, requested_item_ids))
        concatenated_item_names = ', '.join(requested_item_names)
        concatenated_item_quantities = ', '.join(map(str, requested_item_quantities))

        timestamp = datetime.date.today()

        # Generate unique tracking ID
        tracking_id = crud.generate_unique_tracking_id(db)

        new_request = RequestModel(
            user_id=user_id,
            name=user_name,
            date=timestamp,
            year_section=year_section,
            item_id=concatenated_item_ids,
            item_name=concatenated_item_names,
            status="pending",  # Assuming a default status of 'pending'
            user_type=user_type,
            quantity=concatenated_item_quantities,
            tracking_id=tracking_id
        )
        db.add(new_request)
        db.commit()

        # Insert data into request_tracking table
        db.execute(
            text("""
            INSERT INTO request_tracking (name, item_name, date, status, tracking_id)
            VALUES (:name, :item_name, :date, :status, :tracking_id)
            """),
            {
                "name": user_name,
                "item_name": concatenated_item_names,
                "date": timestamp,
                "status": "pending",  # Assuming the status is always 'pending' for new requests
                "tracking_id": tracking_id
            }
        )

        if user_type == "student":
            new_student = Student(student_id=user_id, student_name=user_name, year_section=year_section)
            db.add(new_student)
        elif user_type == "teacher":
            new_teacher = Teacher(teacher_id=user_id, teacher_name=user_name)
            db.add(new_teacher)
        elif user_type == "personnel":
            new_personnel = Personnel(personnel_id=user_id, personnel_name=user_name)
            db.add(new_personnel)

        db.commit()

        return {"message": "Equipment request(s) submitted successfully", "tracking_id": tracking_id}
    except HTTPException as http_exception:
        raise http_exception
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error creating request, possibly due to duplicate tracking ID")
    except Exception as e:
        logger.exception("An error occurred while processing equipment request:")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")