from fastapi import Depends, HTTPException, APIRouter
from .db import get_db

requests = APIRouter(tags=["Requests Tables"])

@requests.get("/requests", response_model=list)
async def get_requests(
    db=Depends(get_db)
):
    query = "SELECT request_id, name, date, item_name, status FROM request"
    db[0].execute(query)
    requests = [
        {"request_id": row[0], "name": row[1], "date": row[2], "item_name": row[3], "status": row[4]}
        for row in db[0].fetchall()
    ]
    return requests

