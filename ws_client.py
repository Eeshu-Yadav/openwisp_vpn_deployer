# ws_client.py

import websocket
import json
from wireguard.handler import handle_wireguard_update
from dotenv import load_dotenv
import os

load_dotenv()
WS_URL = os.getenv("WEBSOCKET_URL")

def on_message(ws, message):
    data = json.loads(message)
    # Check if the update is for WireGuard (customize key as needed)
    if data.get("vpn_backend") == "wireguard":
        print("[WS] Received WireGuard update")
        handle_wireguard_update(data)
    else:
        print("[WS] Ignored update:", data)

def on_error(ws, error):
    print(f"[WS] Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"[WS] Closed: {close_status_code} - {close_msg}")

def on_open(ws):
    print("[WS] Connection established.")

def run_websocket():
    ws = websocket.WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        header={"Authorization": f"Token {os.getenv('API_TOKEN')}"}
    )
    ws.run_forever()

if __name__ == "__main__":
    run_websocket()
