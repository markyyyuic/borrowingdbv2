from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, CheckConstraint, LargeBinary
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
    image = Column(LargeBinary)
    
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
    full_name =  Column(String)
    admin_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    # Add other fields as necessary


class Student(Base):
    __tablename__ = 'student'
    student_id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, index=True)
    year_section = Column(String)

class Teacher(Base):
    __tablename__ = 'teacher'
    teacher_id = Column(Integer, primary_key=True, index=True)
    teacher_name = Column(String, index=True)

class Personnel(Base):
    __tablename__ = 'personnel'
    personnel_id = Column(Integer, primary_key=True, index=True)
    personnel_name = Column(String, index=True)

class Request(Base):
    __tablename__ = 'request'
    request_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    name = Column(String, index=True)
    date = Column(Date)
    year_section = Column(String)
    item_id = Column(String)
    item_name = Column(String)
    quantity = Column(String)
    user_type = Column(String)
    status = Column(String, default="pending") 
    tracking_id = Column(Integer, unique=True, nullable=False)
    
    
