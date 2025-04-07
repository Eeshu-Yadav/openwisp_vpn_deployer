import asyncio
import json
import websockets

async def send_dummy_update(websocket, path=None):
    print("Client connected. Sending dummy update...")
    await asyncio.sleep(2)
    await websocket.send(json.dumps({
        "vpn_backend": "wireguard",
        "vpn_server_id": "test-server-id"
    }))
    await asyncio.sleep(1)
    await websocket.close()

async def main():
    server = await websockets.serve(send_dummy_update, "localhost", 8765)
    print("✅ Dummy WebSocket server running on ws://localhost:8765")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())