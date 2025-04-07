from zerotier.handler import handle_zerotier_update

if __name__ == "__main__":
    print("Simulating a ZeroTier VPN update event...")
    dummy_event = {
        "vpn_backend": "zerotier",
        "vpn_server_id": "test-server-id"
    }
    handle_zerotier_update(dummy_event)
