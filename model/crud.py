from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def create_borrowed_item(db: Session, borrow_item: schemas.BorrowItemCreate):
    db_borrowed_item = models.BorrowedItem(
        item_id=borrow_item.item_id,
        quantity_borrowed=borrow_item.quantity_borrowed,
        borrowers_name=borrow_item.borrowers_name,
        borrow_date=datetime.now(),
        status='borrowed',
        remarks=borrow_item.remarks
    )
    db.add(db_borrowed_item)
    # Assuming you have a proper relationship set up in your models,
    # updating the corresponding Equipment quantity here might not be necessary
    # db.query(models.Equipment).filter(models.Equipment.item_id == borrow_item.item_id).update({
    #     models.Equipment.quantity: models.Equipment.quantity - borrow_item.quantity_borrowed
    # })
    db.commit()
    db.refresh(db_borrowed_item)
    return db_borrowed_item

def update_borrowed_item(db: Session, borrow_id: int, borrow_item: schemas.BorrowItemUpdate):
    db_borrowed_item = db.query(models.BorrowedItem).filter(models.BorrowedItem.borrow_id == borrow_id).first()
    if db_borrowed_item is None:
        return None
    
    # Update the borrowed item with new data
    for key, value in borrow_item.dict(exclude_unset=True).items():
        setattr(db_borrowed_item, key, value)
    
    # Ensure remarks are set to "Returned"
    db_borrowed_item.remarks = "Returned"
    
    db.commit()
    db.refresh(db_borrowed_item)
    return db_borrowed_item
