"""The shell-paint acknowledgement is valid before and after full-app handoff."""

from fastapi.testclient import TestClient

from chappie.core.bus import EventBus
from chappie.core.config import ChappieConfig
from chappie.ui.web.server import WebServer


def test_full_app_accepts_shell_painted_acknowledgement() -> None:
    server = WebServer(ChappieConfig(), bus=EventBus())
    origin = "http://localhost:47821"

    with TestClient(server.app, base_url=origin) as client:
        response = client.post(
            "/api/ui/shell-painted",
            headers={"Origin": origin},
        )

    assert response.status_code == 204
    assert response.content == b""
