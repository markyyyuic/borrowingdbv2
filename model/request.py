from fastapi import Depends, HTTPException, APIRouter, Query
from .db import get_db
from sqlalchemy.orm import Session
import logging
from sqlalchemy import text


requests = APIRouter(tags=["Requests Tables"])
logger = logging.getLogger(__name__)


@requests.post("/request/approve_requests/{request_id}", response_model=dict)
async def approve_request_by_id(
    request_id: int,
    admin_id: int = Query(...),  # Accept admin_id as query parameter
    db: Session = Depends(get_db)
):
    try:
        # Validate admin_id
        query_check_admin = text("SELECT admin_id FROM administrator WHERE admin_id = :admin_id")
        if not db.execute(query_check_admin, {"admin_id": admin_id}).fetchone():
            raise HTTPException(status_code=400, detail="Invalid admin_id")

        # Retrieve approved request data from the request table
        query_select_request = text("""
            SELECT user_id, name, date, year_section, item_name, item_id, quantity
            FROM request
            WHERE request_id = :request_id
        """)
        approved_request_data = db.execute(query_select_request, {"request_id": request_id}).fetchone()

        if not approved_request_data:
            raise HTTPException(status_code=404, detail="Request not found")

        # Deduct the approved quantity from the available quantity of the item in the equipments table
        query_update_quantity = text("""
            UPDATE equipments
            SET quantity = quantity - :quantity
            WHERE item_id = :item_id
        """)
        db.execute(query_update_quantity, {"quantity": approved_request_data[6], "item_id": approved_request_data[5]})
        db.commit()  # Commit the transaction after updating the quantity

        # Check if the quantity is zero and update the status accordingly
        query_check_quantity = text("""
            SELECT quantity
            FROM equipments
            WHERE item_id = :item_id
        """)
        remaining_quantity = db.execute(query_check_quantity, {"item_id": approved_request_data[5]}).fetchone()[0]

        if remaining_quantity == 0:
            # Update the status to "Not Available" if quantity is zero
            query_update_status = text("""
                UPDATE equipments
                SET status = 'Not Available'
                WHERE item_id = :item_id
            """)
            db.execute(query_update_status, {"item_id": approved_request_data[5]})
            db.commit()  # Commit the transaction after updating the status

        # Update status of the approved request to "approved" in the request table
        query_update_status = text("""
            UPDATE request
            SET status = 'approved'
            WHERE request_id = :request_id
        """)
        db.execute(query_update_status, {"request_id": request_id})
        db.commit()  # Commit the transaction after updating the status

        # Insert the approved request data into the reports table
        query_insert_report = text("""
            INSERT INTO reports (request_id, status, name, year_section, item_name)
            VALUES (:request_id, 'approved', :name, :year_section, :item_name)
        """)
        db.execute(query_insert_report, {"request_id": request_id, "name": approved_request_data[1], "year_section": approved_request_data[3], "item_name": approved_request_data[4]})
        db.commit()  # Commit the transaction after inserting into reports table

        # Insert data into the borrowed_items table with a default status 'borrowed'
        query_insert_borrowed_item = text("""
            INSERT INTO borrowed_items (borrowers_name, quantity_borrowed, item_id, borrower_id, item_name, status, admin_id, borrow_date, remarks)
            VALUES (:borrowers_name, :quantity_borrowed, :item_id, :borrower_id, :item_name, :status, :admin_id, :borrow_date, :remarks)
        """)
        db.execute(query_insert_borrowed_item, {
            "borrowers_name": approved_request_data[1],  # borrowers_name (name in request table)
            "quantity_borrowed": approved_request_data[6],  # quantity_borrowed (quantity in request table)
            "item_id": approved_request_data[5],  # item_id (item_id in request table)
            "borrower_id": approved_request_data[0],  # borrower_id (user_id in request table)
            "item_name": approved_request_data[4],  # item_name (item_name in request table)
            "status": 'borrowed',  # Default status for the borrowed item
            "admin_id": admin_id,  # Admin ID
            "borrow_date": approved_request_data[2],  # borrow_date (date in request table)
            "remarks": 'Not Return'
        })

        db.commit()  # Commit the transaction after inserting into borrowed_items table
        # Insert the approved request data into the history table
        query_insert_history = text("""
            INSERT INTO history (name, date, item_name, item_id)
            VALUES (:name, :date, :item_name, :item_id)
        """)
        db.execute(query_insert_history, {"name": approved_request_data[1], "date": approved_request_data[2], "item_name": approved_request_data[4], "item_id": approved_request_data[5]})
        db.commit()  # Commit the transaction after inserting into history table

        # Delete the approved request from the request table
        query_delete_request = text("""
            DELETE FROM request
            WHERE request_id = :request_id
        """)
        db.execute(query_delete_request, {"request_id": request_id})
        db.commit()  # Commit the transaction after deleting the request

        return {"message": "Request approved and moved to history successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the session
        db.close()


@requests.post("/requests/decline_requests/{request_id}", response_model=dict)
async def decline_request_by_id(
    request_id: int,
    db: Session = Depends(get_db)
):
    try:
        # Update status of the declined request to "declined" in the request table
        query_decline_request = text("""
            UPDATE request
            SET status = 'declined'
            WHERE request_id = :request_id
        """)
        db.execute(query_decline_request, {"request_id": request_id})
        db.commit()  # Commit the transaction after updating the status

        # Retrieve declined request data from the request table
        query_select_request = text("""
            SELECT name, date, year_section, item_name, item_id
            FROM request
            WHERE request_id = :request_id
        """)
        declined_request_data = db.execute(query_select_request, {"request_id": request_id}).fetchone()

        if not declined_request_data:
            raise HTTPException(status_code=404, detail="Request not found")

        # Insert the declined request data into the reports table
        query_insert_report = text("""
            INSERT INTO reports (request_id, status, name, year_section, item_name)
            VALUES (:request_id, 'declined', :name, :year_section, :item_name)
        """)
        db.execute(query_insert_report, {"request_id": request_id, "name": declined_request_data[0], "year_section": declined_request_data[2], "item_name": declined_request_data[3]})
        db.commit()  # Commit the transaction after inserting into reports table

        # Insert the declined request data into the history table
        query_insert_history = text("""
            INSERT INTO history (name, date, item_name, item_id)
            VALUES (:name, :date, :item_name, :item_id)
        """)
        db.execute(query_insert_history, {"name": declined_request_data[0], "date": declined_request_data[1], "item_name": declined_request_data[3], "item_id": declined_request_data[4]})
        db.commit()  # Commit the transaction after inserting into history table

        # Delete the declined request from the request table
        query_delete_request = text("""
            DELETE FROM request
            WHERE request_id = :request_id
        """)
        db.execute(query_delete_request, {"request_id": request_id})
        db.commit()  # Commit the transaction after deleting the request

        return {"message": "Request declined and moved to history successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the session
        db.close()
        
@requests.get("/requests", response_model=list)
async def get_requests(db: Session = Depends(get_db)):
    query = text("SELECT request_id, name, date, item_name, status FROM request")
    result = db.execute(query)
    requests = [
        {"request_id": row[0], "name": row[1], "date": row[2], "item_name": row[3], "status": row[4]}
        for row in result.fetchall()
    ]
    return requests