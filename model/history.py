from fastapi import Depends, HTTPException, APIRouter
from .db import get_db

history = APIRouter(tags=["History"])

@history.post("/history/approve_requests/{request_id}", response_model=dict)
async def approve_request_by_id(
    request_id: int,
    db=Depends(get_db)
):
    try:
        # Retrieve approved request data from the request table
        query_select_request = """
            SELECT name, date, year_section, item_name, item_id, quantity
            FROM request
            WHERE request_id = %s
        """
        db[0].execute(query_select_request, (request_id,))
        approved_request_data = db[0].fetchone()

        if not approved_request_data:
            raise HTTPException(status_code=404, detail="Request not found")

        # Deduct the approved quantity from the available quantity of the item in the equipments table
        query_update_quantity = """
            UPDATE equipments
            SET quantity = quantity - %s
            WHERE item_id = %s
        """
        db[0].execute(query_update_quantity, (approved_request_data[5], approved_request_data[4]))
        db[1].commit()  # Commit the transaction after updating the quantity

        # Update status of the approved request to "approved" in the request table
        query_update_status = """
            UPDATE request
            SET status = 'approved'
            WHERE request_id = %s
        """
        db[0].execute(query_update_status, (request_id,))
        db[1].commit()  # Commit the transaction after updating the status

        # Insert the approved request data into the reports table
        query_insert_report = """
            INSERT INTO reports (request_id, status, name, year_section, item_name)
            VALUES (%s, 'approved', %s, %s, %s)
        """
        db[0].execute(query_insert_report, (request_id, approved_request_data[0], approved_request_data[2], approved_request_data[3]))
        db[1].commit()  # Commit the transaction after inserting into reports table

        # Insert the approved request data into the history table
        query_insert_history = """
            INSERT INTO history (name, date, item_name, item_id)
            VALUES (%s, %s, %s, %s)
        """
        db[0].execute(query_insert_history, (approved_request_data[0], approved_request_data[1], approved_request_data[3], approved_request_data[4]))
        db[1].commit()  # Commit the transaction after inserting into history table

        # Delete the approved request from the request table
        query_delete_request = """
            DELETE FROM request
            WHERE request_id = %s
        """
        db[0].execute(query_delete_request, (request_id,))
        db[1].commit()  # Commit the transaction after deleting the request

        return {"message": "Request approved and moved to history successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor and connection
        db[0].close()


@history.post("/history/decline_requests/{request_id}", response_model=dict)
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


@history.get("/history_data", response_model=list)
async def get_history_data(db=Depends(get_db)):
    try:
        # Fetch data from the history table
        query_select_history = """
            SELECT history_id, name, date, item_name, item_id
            FROM history
        """
        db[0].execute(query_select_history)
        history_data = db[0].fetchall()

        return history_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()
