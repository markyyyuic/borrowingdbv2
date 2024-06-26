from pydantic import BaseModel, validator
from datetime import date, datetime
from typing import Optional

class BorrowItemCreate(BaseModel):
    item_id: int
    quantity_borrowed: int
    borrower_id: int
    admin_id: int
    remarks: Optional[str] = None

class BorrowItemUpdate(BaseModel):
    return_date: Optional[date]
    status: Optional[str]
    admin_id: Optional[int] = None
    remarks: Optional[str]
    
    @validator('return_date', pre=True)
    def parse_return_date(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d").date()
        return value

class BorrowItem(BaseModel):
    borrow_id: int
    borrowers_name: str
    item_name: str
    quantity_borrowed: int
    borrow_date: date
    return_date: Optional[date] = None
    remarks: Optional[str] = None

    class Config:
        orm_mode = True




