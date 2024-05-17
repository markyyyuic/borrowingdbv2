from fastapi import Depends, HTTPException, APIRouter
from .db import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text

history = APIRouter(tags=["History"])




@history.get("/history", response_model=list)
async def get_history_data(db: Session = Depends(get_db)):
    try:
        query_select_history = text("SELECT history_id, name, date, item_name FROM history")  # Replace with your actual query
        result = db.execute(query_select_history)
        history_data = [
            {"history_id": row[0], "name": row[1], "date": row[2], "item_name": row[3]}  # Replace with your actual columns
            for row in result.fetchall()
        ]
        return history_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")