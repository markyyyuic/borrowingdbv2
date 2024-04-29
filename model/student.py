from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db
import datetime

students = APIRouter(tags=["Student Information"])


@students.get("/student/student_list", response_model=list)
async def read_student(
    db=Depends(get_db)
):
    query = "SELECT student_ID, student_Name, Year_Section, Borrow_Date_Time, item_ID, item_Name FROM student"
    db[0].execute(query)
    users = [{"student_ID": user[0], "student_Name": user[1], "Year_Section": user[2], "Borrow_Date_Time": user[3],"item_ID": user[4], "item_Name": user[5]} for user in db[0].fetchall()]
    return users

@students.get("/student/get_student", response_model=dict)
async def find_student(
    student_ID: int, 
    db=Depends(get_db)
):
    query = "SELECT student_ID, student_Name, Year_Section, Borrow_Date_Time, item_ID, item_Name FROM student WHERE student_ID = %s"
    db[0].execute(query, (student_ID,))
    user = db[0].fetchone()
    if user:
        return {"student_ID": user[0], "student_Name": user[1], "Year_Section": user[2], "Borrow_Date_Time": user[3],"item_ID": user[4], "item_Name": user[5]}
    raise HTTPException(status_code=404, detail="User not found")


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
    studentID: int , 
    studentName: str = Form(...), 
    year_section: str = Form(...),
    itemID: str = Form(...), 
    itemName: str = Form(...), 
    db=Depends(get_db)
):
    timestamp = datetime.datetime.now()

    query = "UPDATE student SET student_Name = %s,  Year_Section = %s, Borrow_Date_Time = %s, item_ID = %s,  item_Name = %s WHERE student_ID = %s"
    db[0].execute(query, (studentName, year_section, timestamp, itemID, itemName, studentID))
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "student updated successfully"}
    raise HTTPException(status_code=404, detail="student not found")



@students.delete("/student/delete_student", response_model=dict)
async def delete_student(
    student_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the student exists
        query_check_student = "SELECT student_ID FROM student WHERE student_ID = %s"
        db[0].execute(query_check_student, (student_id,))
        existing_student = db[0].fetchone()

        if not existing_student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Delete the student
        query_delete_student = "DELETE FROM student WHERE student_ID = %s"
        db[0].execute(query_delete_student, (student_id,))
        db[1].commit()

        return {"message": "Student deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()
        
        
        
@students.post("/student/request_equipment", response_model=dict)
async def request_equipment(
    student_id: int, 
    item_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the student exists
        query_check_student = "SELECT student_id, student_name, year_section FROM student WHERE student_id = %s"
        db[0].execute(query_check_student, (student_id,))
        student = db[0].fetchone()

        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        student_id, student_name, year_section = student

        # Get the item name based on the item_id
        query_fetch_item_name = "SELECT item_name FROM equipments WHERE item_id = %s"
        db[0].execute(query_fetch_item_name, (item_id,))
        item_name = db[0].fetchone()

        if not item_name:
            raise HTTPException(status_code=404, detail="Item not found")

        item_name = item_name[0]  # Get the item name

        # Insert the request into the request table
        timestamp = datetime.datetime.now()
        query_insert_request = "INSERT INTO request (student_id, name, date, year_section, item_id, item_name) VALUES (%s, %s, %s, %s, %s, %s)"
        db[0].execute(query_insert_request, (student_id, student_name, timestamp, year_section, item_id, item_name))
        db[1].commit()

        # Get student requests including item and student names
        query_student_requests = """
        SELECT r.request_id, r.date, r.item_id, s.student_name, s.year_section, e.item_name
        FROM request AS r
        JOIN student AS s ON r.student_id = s.student_id
        JOIN equipments AS e ON r.item_id = e.item_id
        WHERE r.student_id = %s
        """
        db[0].execute(query_student_requests, (student_id,))
        student_requests = [{
            "request_id": row[0], 
            "date": row[1], 
            "item_id": row[2], 
            "student_name": row[3],
            "year_section": row[4],
            "item_name": row[5]
        } for row in db[0].fetchall()]

        return {"message": "Equipment request submitted successfully", "student_requests": student_requests}
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()


