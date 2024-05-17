from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from .db import get_db
import logging
from sqlalchemy import text
from .db import get_db, fetch_admin_id_from_database
from .schemas import BorrowItemUpdate
from .crud import update_borrowed_item
from sqlalchemy import text
from .db import SessionLocal, engine

logger = logging.getLogger(__name__)
borrowed_items = APIRouter(tags=["Borrowed Items"])

@borrowed_items.post("/borrowed_items/borrow", response_model=schemas.BorrowItem)
async def borrow_equipment(borrow_item: schemas.BorrowItemCreate, db: Session = Depends(get_db)):
    return crud.create_borrowed_item(db=db, borrow_item=borrow_item)


@borrowed_items.put("/borrowed_items/return/{borrow_id}", response_model=schemas.BorrowItem)
async def return_equipment(borrow_id: int, borrow_item: schemas.BorrowItemUpdate, db: Session = Depends(get_db)):
    db_borrowed_item = crud.update_borrowed_item(db=db, borrow_id=borrow_id, borrow_item=borrow_item)
    if not db_borrowed_item:
        raise HTTPException(status_code=404, detail="Borrowed item not found")
    return db_borrowed_item



@borrowed_items.get("/borrowed_list", response_model=list) 
async def get_borrowed_list(db: Session = Depends(get_db)):
    try:
        query = text("""
        SELECT borrow_id, borrowers_name, item_name, quantity_borrowed, borrow_date, return_date, remarks
        FROM borrowed_items
        """)
        result = db.execute(query)
        borrowed_items = [dict(row._mapping) for row in result.fetchall()]  # Convert each row to a dictionary
        
        return borrowed_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database connection
        db.close()
