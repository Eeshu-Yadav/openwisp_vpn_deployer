from wireguard.generator import generate_wg_conf

def test_generate_wg_conf():
    mock_server = {
        "private_key": "abc123",
        "internal_ip": "10.0.0.1/24",
        "port": 51820
    }
    mock_peers = [
        {"public_key": "peerkey1", "internal_ip": "10.0.0.2/32", "endpoint": "1.2.3.4:51820"},
        {"public_key": "peerkey2", "internal_ip": "10.0.0.3/32"}
    ]

    config = generate_wg_conf(mock_server, mock_peers)
    assert "[Interface]" in config
    assert "PrivateKey = abc123" in config
    assert "[Peer]" in config
    assert "AllowedIPs = 10.0.0.2/32" in config
    assert "Endpoint = 1.2.3.4:51820" in config
