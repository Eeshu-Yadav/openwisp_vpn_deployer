from vxlan_wireguard.handler import handle_vxlan_wireguard_update

if __name__ == "__main__":
    print("Simulating a VXLAN over WireGuard update event...")
    dummy_event = {
        "vpn_backend": "vxlan_wireguard",
        "vpn_server_id": "test-server-id"
    }
    handle_vxlan_wireguard_update(dummy_event)
