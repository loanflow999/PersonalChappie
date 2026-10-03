"""Whisper-bar overlay package — the slim default on-screen representation.

``ChappieBarOverlay`` is imported lazily so this package stays importable on a
headless host (no tkinter) for capability probing and tests.
"""
from __future__ import annotations

__all__ = ["ChappieBarOverlay", "NullOverlay"]


def __getattr__(name: str):  # lazy: avoid importing tkinter on headless import
    if name == "ChappieBarOverlay":
        from chappie.ui.chappiebar.overlay import ChappieBarOverlay

        return ChappieBarOverlay
    if name == "NullOverlay":
        from chappie.ui.chappiebar.null_overlay import NullOverlay

        return NullOverlay
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
