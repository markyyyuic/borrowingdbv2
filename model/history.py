from fastapi import Depends, HTTPException, APIRouter
from .db import get_db

history = APIRouter(tags=["History"])




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
