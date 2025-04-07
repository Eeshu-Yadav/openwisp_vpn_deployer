import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Loads from .env in project root

API_URL = os.getenv("OPENWISP_API_URL", "http://localhost:8000/api/v1")
API_TOKEN = os.getenv("API_TOKEN", "dummy_token")
HEADERS = {"Authorization": f"Token {API_TOKEN}"}

def get_vpn_server(server_id):
    """
    Fetch VPN server configuration from OpenWISP Controller.
    Dummy data is returned for testing.
    """
    # For real API call, uncomment below:
    # url = f"{API_URL}/config/vpn/{server_id}/"
    # response = requests.get(url, headers=HEADERS)
    # response.raise_for_status()
    # return response.json()
    
    # Dummy data:
    return {
        "private_key": "dummy_server_private_key",
        "internal_ip": "10.0.0.1/24",
        "port": 51820,
        "vxlan_id": 100,
        "vxlan_group": "239.1.1.1",
        "vxlan_interface": "vxlan0",
        "ca": "ca.pem",
        "cert": "server.crt",
        "key": "server.key",
        "dh": "dh.pem",
        "server_network": "10.8.0.0 255.255.255.0",
        "protocol": "udp"
    }

def get_vpn_peers(server_id):
    """
    Fetch VPN peers for a given VPN server from OpenWISP Controller.
    Dummy data is returned for testing.
    """
    # For real API call, uncomment below:
    # url = f"{API_URL}/config/peers/?vpn={server_id}"
    # response = requests.get(url, headers=HEADERS)
    # response.raise_for_status()
    # return response.json().get("results", [])
    
    # Dummy data:
    return [
        {
            "public_key": "dummy_peer_public_key",
            "internal_ip": "10.0.0.2/32",
            "endpoint": "198.51.100.1:51820"
        }
    ]
