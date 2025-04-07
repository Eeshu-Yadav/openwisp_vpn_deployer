from wireguard.handler import handle_wireguard_update

if __name__ == "__main__":
    print("Simulating a WireGuard VPN update event...")
    dummy_event = {
        "vpn_backend": "wireguard",
        "vpn_server_id": "test-server-id"
    }
    handle_wireguard_update(dummy_event)