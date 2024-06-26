from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model.administrator import administrator
from model.expenses import ExpensesRouter
from model.student import students
from model.teacher import teachers
from model.equipments import equipments
from model.personnel import personnels
from model.history import history
from model.request import requests
from model.borrowed_items import borrowed_items  # Import the borrowed_items router
from model.request_tracker import tracker
app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://entborrowingsystem.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include CRUD routes from modules
app.include_router(administrator, prefix="/adminpanel")
app.include_router(students, prefix="/api")
app.include_router(personnels, prefix="/api")
app.include_router(teachers, prefix="/api")
app.include_router(equipments, prefix="/api")
app.include_router(history, prefix="/history")
app.include_router(requests, prefix="/request")
app.include_router(tracker, prefix="/track")
app.include_router(borrowed_items, prefix="/api")  # Include the borrowed_items router

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
