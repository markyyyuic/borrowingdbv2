# model/expenses.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db

ExpensesRouter = APIRouter(tags=["Test"])

# CRUD operations

@ExpensesRouter.get("/expenses/", response_model=list)
async def read_expenses(
    db=Depends(get_db)
):
    query = "SELECT id, user_id, category_id, amount, description, date FROM expenses"
    db[0].execute(query)
    expenses = [{
                    "id": expense[0], 
                    "user_id": expense[1],
                    "category_id": expense[2],
                    "amount": expense[3],
                    "description": expense[4],
                    "date": expense[5],
                } for expense in db[0].fetchall()]
    return expenses

@ExpensesRouter.get("/expenses/{expense_id}", response_model=dict)
async def read_user(
    expense_id: int, 
    db=Depends(get_db)
):
    query = "SELECT id, user_id, category_id, amount, description, date FROM expenses WHERE id = %s"
    db[0].execute(query, (expense_id,))
    expense = db[0].fetchone()
    if expense:
        return {
                    "id": expense[0], 
                    "user_id": expense[1],
                    "category_id": expense[2],
                    "amount": expense[3],
                    "description": expense[4],
                    "date": expense[5],
                }
    raise HTTPException(status_code=404, detail="User not found")

@ExpensesRouter.post("/expenses/", response_model=dict)
async def create_expense(
    user_id: int = Form(...), 
    category_id: int = Form(...), 
    amount: float = Form(...), 
    description: str = Form(...), 
    date: str = Form(...), 
    db=Depends(get_db)
):

    query = "INSERT INTO expenses (user_id, category_id, amount, description, date) VALUES (%s, %s, %s, %s, %s)"
    db[0].execute(query, (user_id, category_id, amount, description, date))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_expense_id = db[0].fetchone()[0]
    db[1].commit()

    return  {
                    "id": expense[0], 
                    "user_id": expense[1],
                    "category_id": expense[2],
                    "amount": expense[3],
                    "description": expense[4],
                    "date": expense[5],
                }

@ExpensesRouter.put("/expenses/{expense_id}", response_model=dict)
async def update_expense(
    user_id: int = Form(...), 
    category_id: int = Form(...), 
    amount: float = Form(...), 
    description: str = Form(...), 
    date: str = Form(...), 
    db=Depends(get_db)
):

    # Update expense information in the database 
    query = "UPDATE expenses SET user_id = %s, category_id = %s, amount = %s, description = %s, date = %s WHERE id = %s"
    db[0].execute(query, (user_id, category_id, amount, description, date, expense_id))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Expense updated successfully"}
    
    # If no rows were affected, expense not found
    raise HTTPException(status_code=404, detail="Expense not found")

@ExpensesRouter.delete("/expenses/{expense_id}", response_model=dict)
async def delete_expense(
    id: int,
    db=Depends(get_db)
):
    try:
        # Check if the user exists
        query_check_user = "SELECT id FROM expenses WHERE id = %s"
        db[0].execute(query_check_user, (expense_id,))
        existing_user = db[0].fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="Expense not found")

        # Delete the user
        query_delete_user = "DELETE FROM expenses WHERE id = %s"
        db[0].execute(query_delete_user, (expense_id,))
        db[1].commit()

        return {"message": "Expense deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()
