from fastapi import Depends, HTTPException, APIRouter
from .db import get_db
import datetime

history = APIRouter(tags=["History"])

@history.post("/approve_requests", response_model=dict)
async def approve_requests(
    approved_requests: list[int],  # List of request IDs to be approved
    db=Depends(get_db)
):
    try:
        if not approved_requests:
            raise HTTPException(status_code=400, detail="No requests to approve")

        # Retrieve approved requests data from the request table
        query_select_requests = """
            SELECT request_id AS history_id, name, date, item_name, item_id
            FROM request
            WHERE request_id IN (%s)
        """
        query_params = ",".join(["%s"] * len(approved_requests))
        query_select_requests = query_select_requests % query_params
        db[0].execute(query_select_requests, tuple(approved_requests))
        approved_requests_data = db[0].fetchall()

        if not approved_requests_data:
            raise HTTPException(status_code=404, detail="No requests found")

        # Insert approved requests into the history table
        query_insert_history = """
            INSERT INTO history (history_id, name, date, item_name, item_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        db[0].executemany(query_insert_history, approved_requests_data)

        # Delete approved requests from the request table
        query_delete_requests = """
            DELETE FROM request
            WHERE request_id IN (%s)
        """
        query_delete_requests = query_delete_requests % query_params
        db[0].execute(query_delete_requests, tuple(approved_requests))

        db[1].commit()

        return {"message": "Approved requests moved to history successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
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
