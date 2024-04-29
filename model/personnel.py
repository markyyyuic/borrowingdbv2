from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db
import datetime

personnels = APIRouter(tags=["Personnel Information"])

@personnels.get("/personnel/personnel_list", response_model=list)
async def get_Personnel_List(
    db=Depends(get_db)
):
    query = "SELECT personnel_ID, personnel_Name, Borrow_Date_Time, Item_ID, item_Name FROM personnel"
    db[0].execute(query)
    users = [{"personnel_ID": user[0], "personnel_Name": user[1], "Borrow_Date_Time": user[2],"item_ID": user[3], "Item_Name": user[4]} for user in db[0].fetchall()]
    return users

@personnels.get("/personnel/get_personnel", response_model=dict)
async def read_personnel(
    personnelID: int, 
    db=Depends(get_db)
):
    query = "SELECT personnel_ID, personnel_Name, Borrow_Date_Time, item_ID, item_Name FROM personnel WHERE personnel_ID = %s"
    db[0].execute(query, ( personnelID,))
    user = db[0].fetchone()
    if user:
        return {"personnel_ID": user[0], "personnel_Name": user[1],  "Borrow_Date_Time": user[2],"item_ID": user[3], "item_Name": user[4]}
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
    personnelID: int, 
    personnelName: str = Form(...), 
    itemID: str = Form(...), 
    itemName: str = Form(...), 
    db=Depends(get_db)
):
    # Automatic date and time
    timestamp = datetime.datetime.now()

    query = "UPDATE personnel SET  personnel_Name = %s, Borrow_Date_Time = %s, item_ID = %s,  item_Name = %s WHERE personnel_ID = %s"
    db[0].execute(query, (personnelName, timestamp, itemID, itemName, personnelID))
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "personnel updated successfully"}
    raise HTTPException(status_code=404, detail="student not found")

@personnels.delete("/personnel/delete_personnel", response_model=dict)
async def delete_personnel(
    personnelID: int,
    db=Depends(get_db)
):
    try:
        # Check if the teacher exists
        query_check_teacher = "SELECT personnel_ID FROM personnel WHERE personnel_ID = %s"
        db[0].execute(query_check_teacher, (personnelID,))
        existing_teacher = db[0].fetchone()

        if not existing_teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")

        # Delete the teacher
        query_delete_teacher = "DELETE FROM personnel WHERE personnel_id = %s"
        db[0].execute(query_delete_teacher, (personnelID,))
        db[1].commit()

        return {"message": "personnel deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()



@personnels.post("/personnel/request_equipment", response_model=dict)
async def request_equipment(
    personnel_id: int, 
    item_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the personnel exists
        query_check_personnel = "SELECT personnel_id, personnel_Name FROM personnel WHERE personnel_id = %s"
        db[0].execute(query_check_personnel, (personnel_id,))
        personnel_info = db[0].fetchone()

        if not personnel_info:
            raise HTTPException(status_code=404, detail="Personnel not found")

        personnel_name = personnel_info[1]  # Get the personnel name

        # Get the item name based on the item_id
        query_fetch_item_name = "SELECT item_name FROM equipments WHERE item_id = %s"
        db[0].execute(query_fetch_item_name, (item_id,))
        item_name = db[0].fetchone()

        if not item_name:
            raise HTTPException(status_code=404, detail="Item not found")

        item_name = item_name[0]  # Get the item name

        # Insert the request into the request table
        timestamp = datetime.datetime.now()
        query_insert_request = "INSERT INTO request (personnel_id, name, date, item_id, item_name) VALUES (%s, %s, %s, %s, %s)"
        db[0].execute(query_insert_request, (personnel_id, personnel_name, timestamp, item_id, item_name))
        db[1].commit()

        # Get personnel requests including item and personnel names
        query_personnel_requests = """
        SELECT r.request_id, r.date, r.item_id, p.personnel_Name, e.item_name
        FROM request AS r
        JOIN personnel AS p ON r.personnel_id = p.personnel_id
        JOIN equipments AS e ON r.item_id = e.item_id
        WHERE r.personnel_id = %s
        """
        db[0].execute(query_personnel_requests, (personnel_id,))
        personnel_requests = [{
            "request_id": row[0], 
            "date": row[1], 
            "item_id": row[2], 
            "personnel_name": row[3],
            "item_name": row[4]
        } for row in db[0].fetchall()]

        return {"message": "Equipment request submitted successfully", "personnel_requests": personnel_requests}
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()



