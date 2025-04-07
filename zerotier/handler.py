import os
import subprocess
from api import get_vpn_server
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

ZEROTIER_NETWORK_ID = os.getenv("ZEROTIER_NETWORK_ID")
ZT_CLI = os.getenv("ZEROTIER_CLI_PATH", "/usr/sbin/zerotier-cli")  # default path

def handle_zerotier_update(event_data):
    server_id = event_data.get("vpn_server_id")
    if not server_id:
        print("[ZT] No VPN server ID provided in event data.")
        return

    print(f"[ZT] Syncing ZeroTier config for VPN server: {server_id}")
    try:
        server = get_vpn_server(server_id)
        network_id = server.get("zt_network_id", ZEROTIER_NETWORK_ID)

        # Join the ZeroTier network
        subprocess.run(["sudo", "/usr/sbin/zerotier-cli", "join", network_id])
        print(f"[ZT] Joined ZeroTier network {network_id} successfully.")

        # Authorize member in the controller (if required, via REST API)
        # Implement this if your ZeroTier setup requires approval

    except subprocess.CalledProcessError as e:
        print(f"[ZT] Error while joining ZeroTier network: {e}")
    except Exception as e:
        print(f"[ZT] General error: {e}")
