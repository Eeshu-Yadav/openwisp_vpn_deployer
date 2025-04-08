from cli import parse_cli_arguments

def test_parse_args():
    args = parse_cli_arguments(["--tech", "wireguard", "--token", "abc123"])
    assert args.tech == "wireguard"
    assert args.token == "abc123"
