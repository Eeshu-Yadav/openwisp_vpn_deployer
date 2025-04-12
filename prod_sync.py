import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

BASE_API_URL = os.getenv("OPENWISP_API_URL")
API_TOKEN = os.getenv("API_TOKEN")
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def fetch_all_vpn_configs():
    """
    Fetch all VPN configurations available in the OpenWISP Controller.
    The endpoint returns a JSON object that contains a 'results' list.
    """
    url = f"{BASE_API_URL}/controller/vpn/"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except Exception as e:
        print(f"Error fetching VPN configurations: {e}")
        return []

def process_vpn_configs():
    """
    Process and print information about each VPN configuration.
    In production, the deployer might iterate through these configurations,
    determine which VPN backend is being used, and trigger local updates accordingly.
    """
    vpn_configs = fetch_all_vpn_configs()
    if not vpn_configs:
        print("No VPN configurations found.")
        return

    for vpn in vpn_configs:
        vpn_id = vpn.get("id")
        name = vpn.get("name")
        backend = vpn.get("backend")
        config = vpn.get("config", {})
        
        print(f"VPN ID: {vpn_id}")
        print(f"Name  : {name}")
        print(f"Backend: {backend}")
        if backend.endswith("Wireguard"):
            wireguard_config = config.get("wireguard", [{}])
            print("WireGuard Configuration:")
            for item in wireguard_config:
                print(json.dumps(item, indent=4))
        elif backend.endswith("OpenVpn"):
            print("OpenVPN Configuration:")
            print(json.dumps(config, indent=4))
        print("-" * 50)

if __name__ == "__main__":
    process_vpn_configs()
