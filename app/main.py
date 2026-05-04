from fastapi import FastAPI, APIRouter
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
import os

# Models
class NewUser(BaseModel):
    username: str
    password: str
    email: EmailStr
    org: str | None = None

class UserResponse(BaseModel):
    message: str
    username: str


# Routes
router = APIRouter

@router.post("/register", response_model=UserResponse)
def register(user: NewUser):
    return {
        "message": "New user registered successfully",
        "username": user.username
    }

# App init
app = FastAPI()
app.include_router

@app.get("/")
def root():
    return {"message": "API is running"}