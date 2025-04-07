import asyncio
from vpn_deployer.wireguard import handle_wireguard

dummy_config = {
    "address": "10.20.0.1/24",
    "private_key": "SERVER_PRIVATE_KEY",
    "port": 51820,
    "peers": [
        {
            "public_key": "CLIENT_PUBLIC_KEY",
            "allowed_ips": "10.20.0.2/32",
            "endpoint": "192.168.1.10:51820",
            "persistent_keepalive": 25
        }
    ]
}

async def main():
    await handle_wireguard(dummy_config)

if __name__ == "__main__":
    asyncio.run(main())
