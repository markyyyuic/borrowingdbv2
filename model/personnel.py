from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db
import datetime

personnels = APIRouter(tags=["Personnel Information"])

@personnels.get("/personnel/personnel_list", response_model=list)
async def get_Personnel_List(
    db=Depends(get_db)
):
    query = "SELECT p_id, personnel_id, personnel_name FROM personnel"
    db[0].execute(query)
    users = [{"personnel_id": user[1], "personnel_name": user[2]} for user in db[0].fetchall()]
    return users

@personnels.get("/personnel/get_personnel", response_model=dict)
async def read_personnel(
    p_id: int, 
    db=Depends(get_db)
):
    query = "SELECT p_id, personnel_id, personnel_name FROM personnel WHERE p_id = %s"
    db[0].execute(query, ( p_id,))
    user = db[0].fetchone()
    if user:
        return {"personnel_id": user[1], "personnel_namee": user[2]}
    raise HTTPException(status_code=404, detail="User not found")


@personnels.post("/personnel/insert_personnel", response_model=dict)
async def create_personnel(
    personnel_id : int = Form(...), 
    personnel_name: str = Form(...), 
    db=Depends(get_db)
):
    query = "INSERT INTO personnel (personnel_id, personnel_name) VALUES (%s, %s)"
    db[0].execute(query, (personnel_id, personnel_name))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_teacher_id = db[0].fetchone()[0]
    db[1].commit()
    
    return {"personnel_id": personnel_id, "personnel_name": personnel_name}

@personnels.put("/personnel/edit_personnel", response_model=dict)
async def update_personnel(
    p_id: int, 
    personnel_id: int = Form(...), 
    personnel_name: str = Form(...), 
    db=Depends(get_db)
):
    # Automatic date and time
    timestamp = datetime.datetime.now()

    query = "UPDATE personnel SET  personnel_id = %s, personnel_name = %s  WHERE p_id = %s"
    db[0].execute(query, (personnel_id, personnel_name,p_id))
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "personnel updated successfully"}
    raise HTTPException(status_code=404, detail="student not found")

@personnels.delete("/personnel/delete_personnel", response_model=dict)
async def delete_personnel(
    p_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the teacher exists
        query_check_teacher = "SELECT p_id FROM personnel WHERE p_id = %s"
        db[0].execute(query_check_teacher, (p_id,))
        existing_teacher = db[0].fetchone()

        if not existing_teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")

        # Delete the teacher
        query_delete_teacher = "DELETE FROM personnel WHERE p_id = %s"
        db[0].execute(query_delete_teacher, (p_id,))
        db[1].commit()

        return {"message": "personnel deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()






