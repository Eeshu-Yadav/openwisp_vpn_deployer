# wireguard/generator.py

def generate_wg_conf(server, peers):
    lines = []

    # Server interface configuration
    lines.append("[Interface]")
    lines.append(f"PrivateKey = {server.get('private_key', 'server_private_key_placeholder')}")
    lines.append(f"Address = {server.get('internal_ip', '10.0.0.1/24')}")
    lines.append(f"ListenPort = {server.get('port', 51820)}")
    lines.append("")

    # Peers configuration
    for peer in peers:
        lines.append("[Peer]")
        lines.append(f"PublicKey = {peer.get('public_key', 'peer_public_key_placeholder')}")
        lines.append(f"AllowedIPs = {peer.get('internal_ip', '10.0.0.2/32')}")
        if peer.get("endpoint"):
            lines.append(f"Endpoint = {peer['endpoint']}")
        lines.append("")

    return "\n".join(lines)
