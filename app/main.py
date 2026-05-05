import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
USERNAME = os.getenv("WATTTIME_USERNAME")
PASSWORD = os.getenv("WATTTIME_PASSWORD")
EMAIL = os.getenv("EMAIL")
ORG = os.getenv("ORG") or None

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


def get_account_access(token):
    url = f"{BASE_URL}/v3/my-access"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    print("MY_ACCESS:", response.json())


def main():
    # register() # Run this ONLY once, then comment it out
    token = login()
    get_account_access(token)

if __name__ == "__main__":
    main()
