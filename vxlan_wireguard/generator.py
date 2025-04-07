# Generates the combined VXLAN+WireGuard config

def generate_vxlan_wg_conf(server, peers):
    """
    Generate a combined configuration for VXLAN over WireGuard.
    
    Expected server dictionary keys:
      - private_key: WireGuard server private key.
      - internal_ip: Server IP (e.g., "10.0.0.1/24").
      - port: WireGuard listen port (default 51820).
      - vxlan_id: VXLAN identifier.
      - vxlan_group: Multicast group for VXLAN.
      - vxlan_interface: Name for the VXLAN interface.
    
    Expected each peer dictionary to have:
      - public_key: Peer WireGuard public key.
      - internal_ip: Allowed IP for the peer.
      - endpoint (optional): Endpoint address.
    """
    lines = []

    # WireGuard server interface configuration
    lines.append("[Interface]")
    lines.append(f"PrivateKey = {server.get('private_key', 'server_private_key_placeholder')}")
    lines.append(f"Address = {server.get('internal_ip', '10.0.0.1/24')}")
    lines.append(f"ListenPort = {server.get('port', 51820)}")
    lines.append("")

    # VXLAN configuration section (added as comments for clarity)
    lines.append("# VXLAN configuration")
    lines.append(f"VXLAN_ID = {server.get('vxlan_id', server.get('VXLAN_ID', 100))}")
    lines.append(f"VXLAN_Group = {server.get('vxlan_group', server.get('VXLAN_GROUP', '239.1.1.1'))}")
    lines.append(f"VXLAN_Interface = {server.get('vxlan_interface', server.get('VXLAN_INTERFACE', 'vxlan0'))}")
    lines.append("")

    # Peer configuration for each client
    for peer in peers:
        lines.append("[Peer]")
        lines.append(f"PublicKey = {peer.get('public_key', 'peer_public_key_placeholder')}")
        lines.append(f"AllowedIPs = {peer.get('internal_ip', '10.0.0.2/32')}")
        if peer.get("endpoint"):
            lines.append(f"Endpoint = {peer['endpoint']}")
        lines.append("")

    return "\n".join(lines)
