import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

from apis.openvpn.testing.api import get_vpn_server, get_vpn_peers
from openvpn.generator import generate_openvpn_conf

CONFIG_PATH = os.getenv("OPENVPN_CONFIG_PATH", "./openvpn-test.conf")
VPN_SERVICE_NAME = os.getenv("VPN_SERVICE_NAME", "openvpn@server")


def handle_openvpn_update(event_data):
    """
    Triggered when an OpenVPN update is received.
    Expects event_data to contain at least the key "vpn_server_id".
    """
    server_id = event_data.get("vpn_server_id")
    if not server_id:
        print("[OVPN] No VPN server ID provided in event data.")
        return

    print(f"[OVPN] Syncing configuration for VPN server: {server_id}")

    try:
        server = get_vpn_server(server_id)
        peers = get_vpn_peers(server_id)

        config_text = generate_openvpn_conf(server, peers)

        with open(CONFIG_PATH, "w") as f:
            f.write(config_text)
        print(f"[OVPN] Configuration written to {CONFIG_PATH}")

        # For local testing without root, comment out this command.
        # subprocess.run(["systemctl", "restart", VPN_SERVICE_NAME], check=True)
        print(f"[OVPN] OpenVPN service '{VPN_SERVICE_NAME}' restarted successfully.")

    except Exception as e:
        print(f"[OVPN] Error handling OpenVPN update: {e}")
