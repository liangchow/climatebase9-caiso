import requests
import json
import os
import time
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
USERNAME = os.getenv("WATTTIME_USERNAME")
PASSWORD = os.getenv("WATTTIME_PASSWORD")
EMAIL = os.getenv("EMAIL")
ORG = os.getenv("ORG") or None
_token_cache = {"token": None, "expires_at":0}


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

def get_token():
    now = time.time()
    if _token_cache["token"] and now < _token_cache["expires_at"]:
        return _token_cache["token"]
    token = login()
    _token_cache["token"] = token
    _token_cache["expires_at"] = now + (29*60) # Refresh before 30 minutes expiration
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
        "horizon_hours" : 24,  
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    print(response.json())
    
    with open("output.json", "w") as file:
        json.dump(response.json(), file)


def main():
    # register() # Run this ONLY once, then comment it out
    token = get_token() # Rate limit
    # get_account_access(token)
    get_forecast(token)

if __name__ == "__main__":
    main()
