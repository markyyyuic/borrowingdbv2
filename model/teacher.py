from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db
import datetime

teachers = APIRouter(tags=["Teacher Information"])


@teachers.get("/teacher/teacher_list", response_model=list)
async def get_teacherlist(
    db=Depends(get_db)
):
    query = "SELECT Teacher_ID, Teacher_Name, Borrow_Date_Time, item_ID, item_Name FROM teacher"
    db[0].execute(query)
    users = [{"Teacher_ID": user[0], "Teacher_Name": user[1], "Borrow_Date_Time": user[2],"item_ID": user[3], "item_Name": user[4]} for user in db[0].fetchall()]
    return users

@teachers.get("/teacher/get_teacher", response_model=dict)
async def find_teacher(
    teacherID: int, 
    db=Depends(get_db)
):
    query = "SELECT Teacher_ID, Teacher_Name, Borrow_Date_Time, item_ID, item_Name FROM teacher WHERE Teacher_ID = %s"
    db[0].execute(query, ( teacherID,))
    user = db[0].fetchone()
    if user:
        return {"Teacher_ID": user[0], "Teacher_Name": user[1],  "Borrow_Date_Time": user[2],"item_ID": user[3], "item_Name": user[4]}
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
    teacherID: int, 
    teacherName: str = Form(...), 
    itemID: str = Form(...), 
    itemName: str = Form(...), 
    db=Depends(get_db)
):
    # Automatic date and time
    timestamp = datetime.datetime.now()

    query = "UPDATE teacher SET Teacher_Name = %s, Borrow_Date_Time = %s, item_ID = %s,  item_Name = %s WHERE teacher_ID = %s"
    db[0].execute(query, (teacherName, timestamp, itemID, itemName, teacherID))
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Teacher updated successfully"}
    raise HTTPException(status_code=404, detail="student not found")




@teachers.delete("/teacher/delete_teacher", response_model=dict)
async def delete_teacher(
    teacherID: int,
    db=Depends(get_db)
):
    try:
        # Check if the teacher exists
        query_check_teacher = "SELECT Teacher_ID FROM teacher WHERE Teacher_ID = %s"
        db[0].execute(query_check_teacher, (teacherID,))
        existing_teacher = db[0].fetchone()

        if not existing_teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")

        # Delete the teacher
        query_delete_teacher = "DELETE FROM teacher WHERE Teacher_ID = %s"
        db[0].execute(query_delete_teacher, (teacherID,))
        db[1].commit()

        return {"message": "Teacher deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()
    
    
@teachers.post("/teacher/request_equipment", response_model=dict)
async def request_equipment(
    teacher_id: int, 
    item_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the teacher exists
        query_check_teacher = "SELECT Teacher_ID, Teacher_Name FROM teacher WHERE Teacher_ID = %s"
        db[0].execute(query_check_teacher, (teacher_id,))
        teacher = db[0].fetchone()

        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")

        teacher_name = teacher[1]  # Get the teacher's name

        # Get the item name based on the item_id
        query_fetch_item_name = "SELECT item_name FROM equipments WHERE item_id = %s"
        db[0].execute(query_fetch_item_name, (item_id,))
        item_name = db[0].fetchone()

        if not item_name:
            raise HTTPException(status_code=404, detail="Item not found")

        item_name = item_name[0]  # Get the item name

        # Insert the request into the request table
        timestamp = datetime.datetime.now()
        query_insert_request = "INSERT INTO request (teacher_id, name, date, item_id, item_name) VALUES (%s, %s, %s, %s, %s)"
        db[0].execute(query_insert_request, (teacher_id, teacher_name, timestamp, item_id, item_name))
        db[1].commit()

        # Get teacher requests including item and teacher names
        query_teacher_requests = """
        SELECT r.request_id, r.date, r.item_id, t.teacher_name, e.item_name
        FROM request AS r
        JOIN teacher AS t ON r.teacher_id = t.teacher_id
        JOIN equipments AS e ON r.item_id = e.item_id
        WHERE r.teacher_id = %s
        """
        db[0].execute(query_teacher_requests, (teacher_id,))
        teacher_requests = [{
            "request_id": row[0], 
            "date": row[1], 
            "item_id": row[2], 
            "teacher_name": row[3],
            "item_name": row[4]
        } for row in db[0].fetchall()]

        return {"message": "Equipment request submitted successfully", "teacher_requests": teacher_requests}
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()



