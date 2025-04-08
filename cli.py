#!/usr/bin/env python3
import argparse
import os
import sys
import subprocess
import shutil
import json
import requests
from getpass import getpass
from dotenv import load_dotenv

load_dotenv()

def check_dependency(command):
    """Check if a command exists in the system PATH."""
    if shutil.which(command) is None:
        print(f"Dependency check failed: {command} is not installed.")
        return False
    print(f"Dependency check passed: {command} is installed.")
    return True

def fetch_vpn_servers(api_url, api_token):
    """
    Fetch available VPN servers from the OpenWISP Controller REST API.
    Assumes the API endpoint is /controller/vpn/ and returns a paginated result.
    """
    headers = {"Authorization": f"Bearer {api_token}"}
    try:
        response = requests.get(f"{api_url}/controller/vpn/", headers=headers)
        response.raise_for_status()
        data = response.json()
        servers = data.get("results", [])
        return servers
    except Exception as e:
        print("❌ Error fetching VPN servers:", e)
        return None

def save_config_file(config, filename="setup_config.json"):
    """Save the configuration dictionary to a JSON file."""
    try:
        with open(filename, "w") as f:
            json.dump(config, f, indent=4)
        print(f"✅ Configuration saved to {filename}")
    except Exception as e:
        print("❌ Error saving configuration:", e)

def interactive_setup():
    print("\n🔧 Welcome to the OpenWISP VPN Deployer CLI Setup Utility\n")

    # 1. API Token input (or use from .env if present)
    api_token = os.getenv("API_TOKEN")
    if not api_token:
        api_token = getpass("🔑 Enter your OpenWISP API Token (input hidden): ")

    # 2. OpenWISP API URL (with default from .env or fallback)
    default_api_url = os.getenv("OPENWISP_API_URL", "http://localhost:8000/api/v1")
    api_url = input(f"🌐 Enter OpenWISP API URL [{default_api_url}]: ") or default_api_url

    # 3. Fetch available VPN servers from OpenWISP
    print("\n📡 Fetching available VPN servers from OpenWISP...")
    servers = fetch_vpn_servers(api_url, api_token)
    if servers:
        print("🧩 Available VPN servers:")
        for server in servers:
            print(f"  🆔 ID: {server.get('id')}, Name: {server.get('name', 'Unnamed')}")
    else:
        print("⚠️ No VPN servers found or error fetching servers.")

    # 4. Select VPN technology
    print("\n🛠️ Select VPN technology to deploy:")
    print("  1. OpenVPN")
    print("  2. WireGuard")
    print("  3. WireGuard over VXLAN")
    print("  4. ZeroTier")
    choice = input("Enter your choice (1-4): ").strip()

    vpn_choice = {
        "1": "openvpn",
        "2": "wireguard",
        "3": "wireguard-vxlan",
        "4": "zerotier"
    }.get(choice)

    if not vpn_choice:
        print("❌ Invalid choice. Exiting setup.")
        sys.exit(1)

    # 5. Perform dependency checks
    print("\n🔍 Performing dependency checks...")
    if vpn_choice == "openvpn":
        check_dependency("openvpn")
    elif vpn_choice in ["wireguard", "wireguard-vxlan"]:
        check_dependency("wg-quick")
    elif vpn_choice == "zerotier":
        check_dependency("zerotier-cli")

    # 6. Save configuration
    config = {
        "api_token": api_token,
        "api_url": api_url,
        "vpn_choice": vpn_choice,
    }
    save_config_file(config)
    print("\n✅ Setup completed successfully. You can now use the OpenWISP VPN Deployer.\n")

def main():
    parser = argparse.ArgumentParser(description="OpenWISP VPN Deployer CLI Setup Utility")
    parser.add_argument("--setup", action="store_true", help="Run interactive setup")
    parser.add_argument("--show-config", action="store_true", help="Show saved configuration")

    args = parser.parse_args()

    if args.setup:
        interactive_setup()
    elif args.show_config:
        try:
            with open("setup_config.json", "r") as f:
                config = json.load(f)
            print(json.dumps(config, indent=4))
        except Exception as e:
            print("❌ Error reading configuration:", e)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
