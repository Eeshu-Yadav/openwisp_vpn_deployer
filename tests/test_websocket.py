import asyncio
import json
import pytest
from unittest.mock import patch
from websocket_client import listen_to_vpn_updates

@pytest.mark.asyncio
@patch("websocket_client.handle_wireguard_update")
async def test_websocket_event_handler(mock_wg_handler):
    class DummyWebSocket:
        def __init__(self):
            self.called = False

        async def recv(self):
            if not self.called:
                self.called = True
                return json.dumps({
                    "vpn_backend": "wireguard",
                    "vpn_server_id": "test-server-id"
                })
            await asyncio.sleep(0.1)
            raise asyncio.CancelledError()

        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc, tb): return None

    with patch("websockets.connect", return_value=DummyWebSocket()):
        try:
            await listen_to_vpn_updates()
        except asyncio.CancelledError:
            pass

    mock_wg_handler.assert_called_once()