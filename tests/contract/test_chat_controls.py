"""Cross-platform control schema, tool gate, and native-owner contracts."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, get_args
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from chappie.agent_chat.control_types import COMMANDS, CommandName, CommandRequest, GoalStatus
from chappie.agent_chat.service import AgentChatService
from chappie.agent_chat.store import AgentChatStore
from chappie.core.bus import EventBus
from chappie.core.config import SafetyConfig
from chappie.core.protocols import ToolResult
from chappie.core.tool_read_only import allows_read
from chappie.safety.approval import ApprovalWorkflow
from chappie.safety.risk_tier import RiskTierEvaluator
from chappie.safety.tool_executor import ToolExecutor
from chappie.ui.web.agent_chat_routes import router


@pytest.mark.parametrize("platform", ["Windows", "Linux", "Darwin"])
def test_control_api_is_import_light_and_preserves_sessions(
    platform: str, monkeypatch: Any
) -> None:
    monkeypatch.setattr("platform.system", lambda: platform)
    svc = AgentChatService(AgentChatStore())
    session = svc.create_session(provider="openai", surface="chappie")
    app = FastAPI()
    app.state.agent_chat = svc
    app.include_router(router)
    with TestClient(app) as client:
        catalog = client.get("/api/agent-chat/commands").json()
        assert {row["name"] for row in catalog["commands"]} == set(get_args(CommandName))
        result = client.post(
            f"/api/agent-chat/sessions/{session.session_id}/commands",
            json={
                "command": "plan",
                "request_id": "plan-on",
                "arguments": "",
            },
        )
        assert result.status_code == 200
        assert result.json()["state"]["mode"] == "plan"
        assert (
            client.get(f"/api/agent-chat/sessions/{session.session_id}/control").json()[
                "permission_mode"
            ]
            == "plan"
        )
        assert svc.store.get_session(session.session_id).vendor_session is None


def test_python_sql_and_typescript_control_names_match() -> None:
    root = Path(__file__).resolve().parents[2]
    ts = (root / "chappie/ui/web/frontend/src/lib/chatControlApi.ts").read_text(encoding="utf-8")
    assert len(COMMANDS) == len(get_args(CommandName)) == 16
    for name in get_args(CommandName):
        assert f'"{name}"' in ts
    for status in get_args(GoalStatus):
        assert f'"{status}"' in ts
    with pytest.raises(ValueError):
        CommandRequest(command="unknown", request_id="bad")


class SafeSender:
    name = "society_message_agent"
    risk_tier = "safe"
    is_action_tool = True
    schema: dict[str, Any] = {}

    def __init__(self) -> None:
        self.calls = 0

    async def execute(self, args: Any, ctx: Any) -> ToolResult:
        self.calls += 1
        return ToolResult(True, "sent")


def test_plan_execution_gate_blocks_safe_tier_senders_even_if_whitelisted() -> None:
    async def scenario() -> None:
        bus = EventBus()
        executor = ToolExecutor(bus, RiskTierEvaluator(SafetyConfig()), ApprovalWorkflow(bus))
        tool = SafeSender()
        assert not allows_read(tool)
        result = await executor.execute(
            tool, {}, trace_id=uuid4(), config_snapshot={"chat_read_only": True}
        )
        assert not result.success and tool.calls == 0
        assert "reads only" in result.error

    asyncio.run(scenario())
