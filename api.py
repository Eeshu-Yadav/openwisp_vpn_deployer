# api.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("OPENWISP_API_URL")
TOKEN = os.getenv("API_TOKEN")
HEADERS = {"Authorization": f"Token {TOKEN}"}

# def get_vpn_server(server_id):
#     url = f"{API_URL}/config/vpn/{server_id}/"
#     response = requests.get(url, headers=HEADERS)
#     response.raise_for_status()  # Raise error for bad responses
#     return response.json()

# def get_vpn_peers(server_id):
#     url = f"{API_URL}/config/peers/?vpn={server_id}"
#     response = requests.get(url, headers=HEADERS)
#     response.raise_for_status()
#     return response.json().get("results", [])


# Mock functions for testing
def get_vpn_server(server_id):
    return {
        "private_key": "dummy_server_private_key",
        "internal_ip": "10.0.0.1/24",
        "port": 51820
    }

def get_vpn_peers(server_id):
    return [
        {
            "public_key": "dummy_peer_public_key",
            "internal_ip": "10.0.0.2/32",
            "endpoint": "192.168.1.100:51820"
        }
    ]
