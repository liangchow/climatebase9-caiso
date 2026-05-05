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
    params = {
        "username": USERNAME,
        "password": PASSWORD,
        "email": EMAIL,
        "org": ORG,
    }
    response = requests.post(url, json=params)
    print(response.json())


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
    params = {
        # "region": "CAISO_NORTH",
        # "signal_type" : "co2_moer"  
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    print(response.json())


def get_forecast(token):
    url = f"{BASE_URL}/v3/forecast"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "region": "CAISO_NORTH",
        "signal_type" : "co2_moer",
        "horizon_hours" : 0,  
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    print(response.json())


def main():
    # register() # Run this ONLY once, then comment it out
    token = login()
    # get_account_access(token)
    get_forecast(token)

if __name__ == "__main__":
    main()
