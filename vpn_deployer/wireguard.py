import os
import subprocess
import asyncio

from .logger import get_logger
logger = get_logger('wireguard')

# Constants
WG_INTERFACE = "wg0"
WG_CONFIG_DIR = "/etc/wireguard/"
WG_CONFIG_PATH = os.path.join(WG_CONFIG_DIR, f"{WG_INTERFACE}.conf")


def ensure_wireguard_installed():
    """
    Check if WireGuard is installed by trying to run 'wg --version'
    """
    try:
        subprocess.run(["wg", "--version"], check=True, stdout=subprocess.DEVNULL)
        logger.info("WireGuard is installed.")
    except FileNotFoundError:
        logger.error("'wg' not found. Please install WireGuard (sudo apt install wireguard).")
        raise
    except subprocess.CalledProcessError:
        logger.error("Error checking WireGuard installation.")
        raise


def generate_wg_config(interface_config: dict) -> str:
    """
    Generate a WireGuard config file as a string
    """
    logger.info("Generating WireGuard config from interface data.")

    lines = [
        "[Interface]",
        f"Address = {interface_config['address']}",
        f"PrivateKey = {interface_config['private_key']}",
        f"ListenPort = {interface_config.get('port', 51820)}",
        ""
    ]

    for peer in interface_config.get("peers", []):
        peer_block = [
            "[Peer]",
            f"PublicKey = {peer['public_key']}",
            f"AllowedIPs = {peer['allowed_ips']}",
        ]
        if peer.get("endpoint"):
            peer_block.append(f"Endpoint = {peer['endpoint']}")
        if peer.get("persistent_keepalive"):
            peer_block.append(f"PersistentKeepalive = {peer['persistent_keepalive']}")
        peer_block.append("")
        lines.extend(peer_block)

    return "\n".join(lines)


def write_config_to_file(config_text: str):
    """
    Write the WireGuard config to /etc/wireguard/wg0.conf
    """
    logger.info(f"Writing WireGuard config to: {WG_CONFIG_PATH}")

    try:
        os.makedirs(WG_CONFIG_DIR, exist_ok=True)
        with open(WG_CONFIG_PATH, "w") as config_file:
            config_file.write(config_text)
        os.chmod(WG_CONFIG_PATH, 0o600)  # Secure file permissions
    except Exception as e:
        logger.error(f"Failed to write WireGuard config: {e}")
        raise


def reload_wg_interface():
    """
    Reload the WireGuard interface using wg-quick
    """
    logger.info("Reloading wg0 interface using wg-quick.")

    try:
        subprocess.run(["wg-quick", "down", WG_INTERFACE], check=False)
        subprocess.run(["wg-quick", "up", WG_INTERFACE], check=True)
        logger.info("WireGuard interface reloaded successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to reload wg0: {e}")
        raise


async def handle_wireguard(config: dict):
    """
    Async handler for syncing WireGuard config
    This will be called by the sync manager or CLI
    """
    logger.info("Starting WireGuard config sync...")

    try:
        ensure_wireguard_installed()
        config_text = generate_wg_config(config)
        write_config_to_file(config_text)
        reload_wg_interface()
        logger.info("WireGuard sync complete.")
    except Exception as e:
        logger.error(f"WireGuard sync failed: {e}")
