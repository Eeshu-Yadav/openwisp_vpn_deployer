# Fetches API data, writes config, and restarts the interface

import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load the .env file from the project root (go up one level from vxlan_wireguard folder)
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

from apis.vxlan_wireguard.testing.api import get_vpn_server, get_vpn_peers
from vxlan_wireguard.generator import generate_vxlan_wg_conf

# Read configuration from environment variables
CONFIG_PATH = os.getenv("VXLAN_WG_CONFIG_PATH", "./vxlan-wg-test.conf")
VPN_INTERFACE = os.getenv("VPN_INTERFACE_NAME", "wg0")

def handle_vxlan_wireguard_update(event_data):
    """
    Triggered when a VXLAN over WireGuard update event is received.
    Expects event_data to contain at least the key "vpn_server_id".
    """
    server_id = event_data.get("vpn_server_id")
    if not server_id:
        print("[VXLAN-WG] No VPN server ID provided in event data.")
        return

    print(f"[VXLAN-WG] Syncing configuration for VPN server: {server_id}")

    try:
        # Fetch configuration from the OpenWISP Controller
        server = get_vpn_server(server_id)
        peers = get_vpn_peers(server_id)

        # Generate combined configuration content
        config_text = generate_vxlan_wg_conf(server, peers)

        # Write configuration to file
        with open(CONFIG_PATH, "w") as f:
            f.write(config_text)
        print(f"[VXLAN-WG] Configuration written to {CONFIG_PATH}")

        # For testing, you might comment these out.
        # subprocess.run(["wg-quick", "down", VPN_INTERFACE], stderr=subprocess.DEVNULL)
        # subprocess.run(["wg-quick", "up", VPN_INTERFACE])
        print(f"[VXLAN-WG] WireGuard interface '{VPN_INTERFACE}' restarted successfully.")

    except Exception as e:
        print(f"[VXLAN-WG] Error handling VXLAN over WireGuard update: {e}")
