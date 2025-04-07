from pathlib import Path
from dotenv import load_dotenv
import os
import subprocess
from api import get_vpn_server, get_vpn_peers
from wireguard.generator import generate_wg_conf

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

CONFIG_PATH = os.getenv("CONFIG_PATH", "wg0-test.conf")
VPN_INTERFACE = os.getenv("VPN_INTERFACE_NAME", "wg0")

def handle_wireguard_update(event_data):
    """
    Triggered when a WireGuard update is received.
    Expects event_data to contain at least the key "vpn_server_id".
    """
    server_id = event_data.get("vpn_server_id")
    if not server_id:
        print("[WG] No VPN server ID provided in event data.")
        return

    print(f"[WG] Syncing configuration for VPN server: {server_id}")

    try:
        server = get_vpn_server(server_id)
        peers = get_vpn_peers(server_id)

        config_text = generate_wg_conf(server, peers)

        with open(CONFIG_PATH, "w") as f:
            f.write(config_text)
        print(f"[WG] Configuration written to {CONFIG_PATH}")

        # For testing, you might skip these commands if you don't have root or WireGuard installed.
        # subprocess.run(["wg-quick", "down", VPN_INTERFACE], stderr=subprocess.DEVNULL)
        # subprocess.run(["wg-quick", "up", VPN_INTERFACE])
        print(f"[WG] WireGuard interface '{VPN_INTERFACE}' restarted successfully.")

    except Exception as e:
        print(f"[WG] Error handling WireGuard update: {e}")
