from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .db import get_db
from sqlalchemy import text

tracker = APIRouter(tags=["Tracking Tables"])

@tracker.get("/request_tracking/get_tracker", response_model=dict)
async def find_tracker(tracking_id: int, db: Session = Depends(get_db)):
    query = text("SELECT tracking_id, name, item_name, date, status FROM request_tracking WHERE tracking_id = :tracking_id")
    tracker_info = db.execute(query, {"tracking_id": tracking_id}).fetchone()
    if tracker_info:
        return {
            "tracking_id": tracker_info[0],
            "name": tracker_info[1],
            "item_name": tracker_info[2],
            "date": tracker_info[3],
            "status": tracker_info[4]
        }
    raise HTTPException(status_code=404, detail="Tracker not found")


@tracker.get("/get_trackerlist", response_model=list)
async def get_tracker(db: Session = Depends(get_db)):
    query = text("SELECT tracking_id, name, item_name, date, status FROM request_tracking")
    result = db.execute(query)
    tracker_data = [
        {"tracking_id": row[0], "name": row[1], "item_name": row[2], "date": row[3], "status": row[4]}
        for row in result.fetchall()
    ]
    return tracker_data