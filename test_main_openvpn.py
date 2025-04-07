from openvpn.handler import handle_openvpn_update

if __name__ == "__main__":
    print("Simulating an OpenVPN update event...")
    dummy_event = {
        "vpn_backend": "openvpn",
        "vpn_server_id": "test-server-id"
    }
    handle_openvpn_update(dummy_event)