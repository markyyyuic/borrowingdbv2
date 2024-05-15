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
    db=Depends(get_db)
):
    try:
        # Unpack the db tuple to get the cursor and connection
        cursor, conn = db

        # Validate admin_id
        query_check_admin = "SELECT admin_id FROM administrator WHERE admin_id = %s"
        cursor.execute(query_check_admin, (admin_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=400, detail="Invalid admin_id")

        # Retrieve approved request data from the request table
        query_select_request = """
            SELECT user_id, name, date, year_section, item_name, item_id, quantity
            FROM request
            WHERE request_id = %s
        """
        cursor.execute(query_select_request, (request_id,))
        approved_request_data = cursor.fetchone()

        if not approved_request_data:
            raise HTTPException(status_code=404, detail="Request not found")

        # Deduct the approved quantity from the available quantity of the item in the equipments table
        query_update_quantity = """
            UPDATE equipments
            SET quantity = quantity - %s
            WHERE item_id = %s
        """
        cursor.execute(query_update_quantity, (approved_request_data[6], approved_request_data[5]))
        conn.commit()  # Commit the transaction after updating the quantity

        # Check if the quantity is zero and update the status accordingly
        query_check_quantity = """
            SELECT quantity
            FROM equipments
            WHERE item_id = %s
        """
        cursor.execute(query_check_quantity, (approved_request_data[5],))
        remaining_quantity = cursor.fetchone()[0]

        if remaining_quantity == 0:
            # Update the status to "Not Available" if quantity is zero
            query_update_status = """
                UPDATE equipments
                SET status = 'Not Available'
                WHERE item_id = %s
            """
            cursor.execute(query_update_status, (approved_request_data[5],))
            conn.commit()  # Commit the transaction after updating the status

        # Update status of the approved request to "approved" in the request table
        query_update_status = """
            UPDATE request
            SET status = 'approved'
            WHERE request_id = %s
        """
        cursor.execute(query_update_status, (request_id,))
        conn.commit()  # Commit the transaction after updating the status

        # Insert the approved request data into the reports table
        query_insert_report = """
            INSERT INTO reports (request_id, status, name, year_section, item_name)
            VALUES (%s, 'approved', %s, %s, %s)
        """
        cursor.execute(query_insert_report, (request_id, approved_request_data[1], approved_request_data[3], approved_request_data[4]))
        conn.commit()  # Commit the transaction after inserting into reports table

        # Insert data into the borrowed_items table with a default status 'borrowed'
        query_insert_borrowed_item = """
            INSERT INTO borrowed_items (borrowers_name, quantity_borrowed, item_id, borrower_id, item_name, status, admin_id, borrow_date, remarks)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query_insert_borrowed_item, (
            approved_request_data[1],  # borrowers_name (name in request table)
            approved_request_data[6],  # quantity_borrowed (quantity in request table)
            approved_request_data[5],  # item_id (item_id in request table)
            approved_request_data[0],  # borrower_id (user_id in request table)
            approved_request_data[4],  # item_name (item_name in request table)
            'borrowed',  # Default status for the borrowed item
            admin_id,  # Admin ID
            approved_request_data[2],  # borrow_date (date in request table)
            'Not Return'
        ))

        conn.commit()  # Commit the transaction after inserting into borrowed_items table
        # Insert the approved request data into the history table
        query_insert_history = """
            INSERT INTO history (name, date, item_name, item_id)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query_insert_history, (approved_request_data[1], approved_request_data[2], approved_request_data[4], approved_request_data[5]))
        conn.commit()  # Commit the transaction after inserting into history table

        # Delete the approved request from the request table
        query_delete_request = """
            DELETE FROM request
            WHERE request_id = %s
        """
        cursor.execute(query_delete_request, (request_id,))
        conn.commit()  # Commit the transaction after deleting the request

        return {"message": "Request approved and moved to history successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()




@requests.post("/history/decline_requests/{request_id}", response_model=dict)
async def decline_request_by_id(
    request_id: int,
    db=Depends(get_db)
):
    try:
        # Update status of the declined request to "declined" in the request table
        query_decline_request = """
            UPDATE request
            SET status = 'declined'
            WHERE request_id = %s
        """
        db[0].execute(query_decline_request, (request_id,))
        db[1].commit()  # Commit the transaction after updating the status

        # Retrieve declined request data from the request table
        query_select_request = """
            SELECT name, date, year_section, item_name, item_id
            FROM request
            WHERE request_id = %s
        """
        db[0].execute(query_select_request, (request_id,))
        declined_request_data = db[0].fetchone()

        if not declined_request_data:
            raise HTTPException(status_code=404, detail="Request not found")

        # Insert the declined request data into the reports table
        query_insert_report = """
            INSERT INTO reports (request_id, status, name, year_section, item_name)
            VALUES (%s, 'declined', %s, %s, %s)
        """
        db[0].execute(query_insert_report, (request_id, declined_request_data[0], declined_request_data[2], declined_request_data[3]))
        db[1].commit()  # Commit the transaction after inserting into reports table

        # Insert the declined request data into the history table
        query_insert_history = """
            INSERT INTO history (name, date, item_name, item_id)
            VALUES (%s, %s, %s, %s)
        """
        db[0].execute(query_insert_history, (declined_request_data[0], declined_request_data[1], declined_request_data[3], declined_request_data[4]))
        db[1].commit()  # Commit the transaction after inserting into history table

        # Delete the declined request from the request table
        query_delete_request = """
            DELETE FROM request
            WHERE request_id = %s
        """
        db[0].execute(query_delete_request, (request_id,))
        db[1].commit()  # Commit the transaction after deleting the request

        return {"message": "Request declined and moved to history successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor and connection
        db[0].close()
        
@requests.get("/requests", response_model=list)
async def get_requests(db: Session = Depends(get_db)):
    query = text("SELECT request_id, name, date, item_name, status FROM request")
    result = db.execute(query)
    requests = [
        {"request_id": row[0], "name": row[1], "date": row[2], "item_name": row[3], "status": row[4]}
        for row in result.fetchall()
    ]
    return requests