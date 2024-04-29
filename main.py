# main.py
from fastapi import FastAPI
from model.administrator import administrator
# from model.account import accounts
from model.expenses import ExpensesRouter
from model.student import students
from model.teacher import teachers
from model.equipments import equipments
from fastapi.middleware.cors import CORSMiddleware
from model.personnel import personnels
from model.history import history


app = FastAPI()

origins = [
    "http://localhost:5173/",
    "https://entborrowingsystem.netlify.app/",  # Assuming your Vue.js server runs on port 8080
]

# Include CRUD routes from modules


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(administrator,  prefix="/adminpanel")
app.include_router(students,  prefix="/api")
app.include_router(teachers,  prefix="/api")
app.include_router(equipments,  prefix="/api")
app.include_router(personnels,  prefix="/api")
app.include_router(history,  prefix="/history")





