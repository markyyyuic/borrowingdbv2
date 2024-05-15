from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Equipment(Base):
    __tablename__ = 'equipments'
    item_id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, index=True)
    quantity = Column(Integer)
    status = Column(String)
    admin_id = Column(Integer)
    last_editor_id = Column(Integer)
    latest_editor = Column(String)
    last_editor = Column(String)
    
class BorrowedItem(Base):
    __tablename__ = 'borrowed_items'

    borrow_id = Column(Integer, primary_key=True, index=True)  # Assuming the primary key is named borrow_id
    borrowers_name = Column(String, index=True)
    item_name = Column(String, index=True)
    quantity_borrowed = Column(Integer)
    borrow_date = Column(Date)
    return_date = Column(Date, nullable=True)
    remarks = Column(String, nullable=True)
    item_id = Column(Integer, ForeignKey('equipments.item_id'))  # Assuming item_id is the foreign key to equipments.item_id

    item_id = Column(Integer, ForeignKey('equipments.item_id'))
    item = relationship("Equipment", backref="borrowed_items")

    __table_args__ = (
        CheckConstraint("status IN ('borrowed', 'returned')"),
    )

class Administrator(Base):
    __tablename__ = 'administrator'

    admin_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    # Add other fields as necessary
