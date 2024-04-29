# model/categories.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db

accounts = APIRouter(tags=["Student Information"])

# CRUD operations

@accounts.get("/student/", response_model=list)
async def read_student(
    db=Depends(get_db)
):
    query = "SELECT Student_ID, student_Name FROM student"
    db[0].execute(query)
    categories = [{"Student_ID": student[0], "student_Name": student[1]} for student in db[0].fetchall()]
    return categories

@accounts.get("/student/{Student_ID}", response_model=dict)
async def read_student(
    Student_ID: int, 
    db=Depends(get_db)
):
    query = "SELECT Student_ID, student_Name FROM student WHERE Student_ID = %s"
    db[0].execute(query, (Student_ID,))
    student = db[0].fetchone()
    if student:
        return {"Student_ID": student[0], "student_Name": student[1]}
    raise HTTPException(status_code=404, detail="student not found")

@accounts.post("/student/", response_model=dict)
async def create_category(
    student_name: str = Form(...), 
    db=Depends(get_db)
):
    query = "INSERT INTO student (student_name) VALUES (%s)"
    db[0].execute(query, (student_name))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_student_id = db[0].fetchone()[0]
    db[1].commit()

    return {"Student_ID": new_student_id, "student_Name": name}

@accounts.put("/student/{Student_ID}", response_model=dict)
async def update_category(
    Student_ID: int,
    student_name: str = Form(...),
    db=Depends(get_db)
):
    # Update category information in the database 
    query = "UPDATE student SET student_name = %s WHERE Student_ID = %s"
    db[0].execute(query, (student_name, Student_ID))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Student details updated successfully"}
    
    # If no rows were affected, category not found
    raise HTTPException(status_code=404, detail="Category not found")

@accounts.delete("/categories/{category_id}", response_model=dict)
async def delete_category(
    category_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the category exists
        query_check_category = "SELECT id FROM categories WHERE id = %s"
        db[0].execute(query_check_category, (category_id,))
        existing_category = db[0].fetchone()

        if not existing_category:
            raise HTTPException(status_code=404, detail="Category not found")

        # Delete the category
        query_delete_category = "DELETE FROM categories WHERE id = %s"
        db[0].execute(query_delete_category, (category_id,))
        db[1].commit()

        return {"message": "Category deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()

