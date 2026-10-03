"""Chappie-Agent registry — live tree of all active Chappie-Agents.

Subscribes to the EventBus and builds an in-memory tree from the Phase-5.5
instrumentation events (ChappieAgentTaskStarted/Completed, BrainTurnStarted/
Completed, ToolCallStarted/Completed, HarnessDispatched/Completed).
Consumed by the desktop app canvas view via the API
``GET /api/sub-agents/tree``.
"""
from .registry import AgentNode, ChappieAgentRegistry

__all__ = ["AgentNode", "ChappieAgentRegistry"]
