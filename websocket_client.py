import asyncio
import json
import websockets
from dotenv import load_dotenv
import os

from wireguard.handler import handle_wireguard_update
from openvpn.handler import handle_openvpn_update
from zerotier.handler import handle_zerotier_update
from vxlan_wireguard.handler import handle_vxlan_wireguard_update

# Load environment variables
load_dotenv()
WEBSOCKET_URL = os.getenv("WEBSOCKET_URL", "wss://openwisp.example.com/ws/vpn-updates/")

async def listen_to_vpn_updates():
    try:
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            print(f"[WS] Connected to WebSocket at {WEBSOCKET_URL}")

            while True:
                message = await websocket.recv()
                data = json.loads(message)

                vpn_type = data.get("vpn_backend")
                print(f"[WS] Received event: {vpn_type}")

                if vpn_type == "wireguard":
                    handle_wireguard_update(data)
                elif vpn_type == "openvpn":
                    handle_openvpn_update(data)
                elif vpn_type == "zerotier":
                    handle_zerotier_update(data)
                elif vpn_type == "wireguard-vxlan":
                    handle_vxlan_wireguard_update(data)
                else:
                    print(f"[WS] Unsupported VPN backend: {vpn_type}")

    except Exception as e:
        print(f"[WS] Error connecting to WebSocket: {e}")

if __name__ == "__main__":
    asyncio.run(listen_to_vpn_updates())
