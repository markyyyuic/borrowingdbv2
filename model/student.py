from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db
import datetime

students = APIRouter(tags=["Student Information"])


@students.get("/student/student_list", response_model=list)
async def read_student(
    db=Depends(get_db)
):
    query = "SELECT s_id, student_id, student_name, year_section FROM student"
    db[0].execute(query)
    users = [{ "student_id": user[1], "student_name": user[2], "year_section": user[3]} for user in db[0].fetchall()]
    return users

@students.get("/student/get_student", response_model=dict)
async def find_student(
    s_id: int, 
    db=Depends(get_db)
):
    query = "SELECT  s_id, student_id, student_name, year_section FROM student WHERE s_id = %s"
    db[0].execute(query, (s_id,))
    user = db[0].fetchone()
    if user:
        return {"student_id": user[1], "student_name": user[2], "year_section": user[3]}
    raise HTTPException(status_code=404, detail="Student not found")


@students.post("/student/insert_student", response_model=dict)
async def create_student(
    student_id: int = Form(...), 
    student_name: str = Form(...), 
    year_section: str = Form(...),
    db=Depends(get_db)
):
    # Automatic date and time
    timestamp = datetime.datetime.now()

    query = "INSERT INTO student (student_id, student_name, year_section) VALUES (%s, %s, %s)"
    db[0].execute(query, (student_id, student_name, year_section))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_user_id = db[0].fetchone()[0]
    db[1].commit()
    
    return {"student_id": student_id, "student_name": student_name, "year_section": year_section}


@students.put("/student/edit_student", response_model=dict)
async def edit_student(
    s_id: int , 
    student_id: int = Form(...),
    student_name: str = Form(...), 
    year_section: str = Form(...),
    db=Depends(get_db)
):
   

    query = "UPDATE student   SET student_id = %s,  student_name = %s, year_section = %s WHERE s_id = %s"
    db[0].execute(query, (student_id, student_name, year_section, s_id))
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Student updated successfully"}
    raise HTTPException(status_code=404, detail="student not found")



@students.delete("/student/delete_student", response_model=dict)
async def delete_student(
    s_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the student exists
        query_check_student = "SELECT s_id FROM student WHERE s_id = %s"
        db[0].execute(query_check_student, (s_id,))
        existing_student = db[0].fetchone()

        if not existing_student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Delete the student
        query_delete_student = "DELETE FROM student WHERE s_id = %s"
        db[0].execute(query_delete_student, (s_id,))
        db[1].commit()

        return {"message": "Student deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()
        
        
        



