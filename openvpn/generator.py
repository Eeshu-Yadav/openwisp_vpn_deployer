def generate_openvpn_conf(server, peers):
    """
    Generate the OpenVPN configuration file content.

    `server` is a dict containing server configuration:
      - port: OpenVPN port (default 1194)
      - protocol: Protocol, e.g., 'udp' (default 'udp')
      - ca, cert, key, dh: File names for the certificate authority, server certificate,
        server key, and Diffie-Hellman parameters (with defaults provided)
      - server_network: Network and netmask for VPN clients (default "10.8.0.0 255.255.255.0")
    
    `peers` is a list of peer configurations, which might be used for generating CCD files
    (not used directly in the main server configuration).
    """
    lines = []
    lines.append("port " + str(server.get('port', 1194)))
    lines.append("proto " + server.get('protocol', "udp"))
    lines.append("dev tun")
    lines.append(f"ca {server.get('ca', 'ca.pem')}")
    lines.append(f"cert {server.get('cert', 'server.crt')}")
    lines.append(f"key {server.get('key', 'server.key')}")
    lines.append(f"dh {server.get('dh', 'dh.pem')}")
    lines.append("server " + server.get('server_network', "10.8.0.0 255.255.255.0"))
    lines.append("ifconfig-pool-persist ipp.txt")
    lines.append("keepalive 10 120")
    lines.append("persist-key")
    lines.append("persist-tun")
    lines.append("status openvpn-status.log")
    lines.append("verb 3")
    return "\n".join(lines)
