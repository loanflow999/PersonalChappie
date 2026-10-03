"""The REST/WS readiness promises match the desktop capability on every OS."""

import pytest
from fastapi.testclient import TestClient

from chappie.core.bus import EventBus
from chappie.core.config import ChappieConfig
from chappie.core.events import VoiceBootStatus
from chappie.ui.web.schema import event_to_ws_envelope
from chappie.ui.web.server import WebServer


@pytest.mark.asyncio
async def test_ready_transport_matches_actual_voice_capability(monkeypatch):
    monkeypatch.delenv("CHAPPIE_VOICE", raising=False)
    bus = EventBus()
    server = WebServer(ChappieConfig(), bus=bus)
    client = TestClient(server.app)
    for detail, ready, expected in [
        ("warmup_start", False, False),
        ("watchdog_timeout", True, False),
        ("voice_unavailable", True, False),
        ("listening", True, True),
        ("warmup_start", False, False),
    ]:
        event = VoiceBootStatus(ready=ready, detail=detail)
        await bus.publish(event)
        assert event_to_ws_envelope(event)["payload"]["ready"] is expected
        assert client.get("/api/voice/status").json()["ready"] is expected
        assert event.voice_usable is expected
