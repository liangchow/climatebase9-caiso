import requests
import os
# from typing import Optional
# from fastapi import FastAPI
# from pydantic import BaseModel, EmailStr
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
USERNAME = os.getenv("WATTTIME_USERNAME")
PASSWORD = os.getenv("WATTTIME_PASSWORD")
EMAIL = os.getenv("EMAIL")
ORG = os.getenv("ORG") or None

# Models
# class NewUser(BaseModel):
#     username: str
#     password: str
#     email: EmailStr
#     org: Optional[str] = None

# class UserResponse(BaseModel):
#     message: str
#     username: str

# App init
# app = FastAPI()

# @app.get("/")
# def root():
#     return {"message": "API is running"}

# @app.post("/register", response_model=UserResponse)
# def register(user: NewUser):
#     url = f"{BASE_URL}/register"
#     params = {'username': USERNAME,
#               'password': PASSWORD,
#               'email': EMAIL,
#               'org': ORG}
#     response = requests.post(url, params=params)
#     response.raise_for_status()
#     return {
#         "message": "New user registered successfully",
#         "username": USERNAME
#     }

def register():
    url = f"{BASE_URL}/register"
    payload = {
        "username": USERNAME,
        "password": PASSWORD,
        "email": EMAIL,
        "org": ORG,
    }
    response = requests.post(url, json=payload)
    print("REGISTER:", response.json())


def login():
    url = f"{BASE_URL}/login"
    response = requests.get(
        url,
        auth=HTTPBasicAuth(USERNAME, PASSWORD)
    )
    data = response.json()
    token = data.get("token")
    if not token:
        raise Exception(f"Login failed: {data}")
    return token


def get_index(token):
    url = f"{BASE_URL}/index"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "ba": "CAISO_NORTH"
    }
    response = requests.get(url, headers=headers, params=params)
    print("INDEX:", response.json())


def main():
    # register() # Run this ONLY once, then comment it out
    token = login()
    get_index(token)

if __name__ == "__main__":
    main()