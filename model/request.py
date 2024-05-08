from fastapi import Depends, HTTPException, APIRouter
from .db import get_db

requests = APIRouter(tags=["Requests Tables"])

@requests.get("/requests/student/{student_id}", response_model=list)
async def get_student_requests(
    student_id: int, 
    db=Depends(get_db)
):
    query = "SELECT request_id, date, item_id, name, item_name FROM request WHERE student_id = %s"
    db[0].execute(query, (student_id,))
    student_requests = [{"request_id": row[0], "date": row[1], "item_id": row[2],"name": row[3], "item_name": row[4]} for row in db[0].fetchall()]
    return student_requests

@requests.get("/requests/teacher/{teacher_id}", response_model=list)
async def get_teacher_requests(
    teacher_id: int, 
    db=Depends(get_db)
):
    query = "SELECT request_id, date, item_id, name, item_name FROM request WHERE teacher_id = %s"
    db[0].execute(query, (teacher_id,))
    teacher_requests = [{"request_id": row[0], "date": row[1], "item_id": row[2], "name": row[3], "item_name": row[4]} for row in db[0].fetchall()]
    return teacher_requests

@requests.get("/requests/personnel/{personnel_id}", response_model=list)
async def get_personnel_requests(
    personnel_id: int, 
    db=Depends(get_db)
):
    query = "SELECT request_id, date, item_id, name, item_name FROM request WHERE personnel_id = %s"
    db[0].execute(query, (personnel_id,))
    personnel_requests = [{"request_id": row[0], "date": row[1], "item_id": row[2], "name": row[3],"item_name": row[4]} for row in db[0].fetchall()]
    return personnel_requests

@requests.get("/requests/equipment/{item_id}", response_model=list)
async def get_equipment_requests(
    item_id: int, 
    db=Depends(get_db)
):
    query = "SELECT request_id, date, student_id, teacher_id, personnel_id, item_name FROM request WHERE item_id = %s"
    db[0].execute(query, (item_id,))
    equipment_requests = [{"request_id": row[0], "date": row[1], "student_id": row[2], "teacher_id": row[3], "personnel_id": row[4], "item_name": row[5]} for row in db[0].fetchall()]
    return equipment_requests


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

