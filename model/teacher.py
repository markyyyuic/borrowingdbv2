from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db
import datetime

teachers = APIRouter(tags=["Teacher Information"])


@teachers.get("/teacher/teacher_list", response_model=list)
async def get_teacherlist(
    db=Depends(get_db)
):
    query = "SELECT t_id, teacher_id, teacher_name FROM teacher"
    db[0].execute(query)
    users = [{"teacher_id": user[0], "teacher_name": user[1]} for user in db[0].fetchall()]
    return users

@teachers.get("/teacher/get_teacher", response_model=dict)
async def find_teacher(
    teacherID: int, 
    db=Depends(get_db)
):
    query = "SELECT t_id, teacher_id, teacher_name FROM teacher WHERE t_id = %s"
    db[0].execute(query, ( teacherID,))
    user = db[0].fetchone()
    if user:
        return {"teacher_id": user[0], "teacher_name": user[1]}
    raise HTTPException(status_code=404, detail="User not found")


@teachers.post("/teacher/add_teacher", response_model=dict)
async def adding_teacher(
    teacher_id: int = Form(...), 
    teacher_name: str = Form(...), 
    db=Depends(get_db)
):
    # Automatic date and time
    timestamp = datetime.datetime.now()

    query = "INSERT INTO teacher (teacher_id, teacher_name) VALUES (%s, %s)"
    db[0].execute(query, (teacher_id, teacher_name))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_user_id = db[0].fetchone()[0]
    db[1].commit()
    
    return {"teacher_id": teacher_id, "teacher_name": teacher_name}


@teachers.put("/teacher/edit_teacher", response_model=dict)
async def updating_teacher(
    teacher_id: int, 
    teacher_name: str = Form(...), 
 
    db=Depends(get_db)
):
    # Automatic date and time
    timestamp = datetime.datetime.now()

    query = "UPDATE teacher SET teacher_id = %s, teacher_name = %s WHERE t_id = %s"
    db[0].execute(query, (teacher_id, teacher_name))
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Teacher updated successfully"}
    raise HTTPException(status_code=404, detail="student not found")




@teachers.delete("/teacher/delete_teacher", response_model=dict)
async def delete_teacher(
    t_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the teacher exists
        query_check_teacher = "SELECT t_id FROM teacher WHERE t_id = %s"
        db[0].execute(query_check_teacher, (t_id,))
        existing_teacher = db[0].fetchone()

        if not existing_teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")

        # Delete the teacher
        query_delete_teacher = "DELETE FROM teacher WHERE t_id = %s"
        db[0].execute(query_delete_teacher, (t_id,))
        db[1].commit()

        return {"message": "Teacher deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()
    
    