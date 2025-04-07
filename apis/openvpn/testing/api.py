def get_vpn_server(server_id):
    return {
        "port": 1194,
        "protocol": "udp",
        "ca": "ca.pem",
        "cert": "server.crt",
        "key": "server.key",
        "dh": "dh.pem",
        "server_network": "10.8.0.0 255.255.255.0"
    }

def get_vpn_peers(server_id):
    return []