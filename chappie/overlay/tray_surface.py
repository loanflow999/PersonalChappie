"""``TrayOnlySurface`` — the universal overlay floor (Wave 2, sub-task 2.6; AD-11).

When no transparent orb can be drawn (headless VPS, Wayland, a Linux compositor
that fails the color-key probe, or simply no Tk), the orb degrades to the
already-cross-platform pystray tray (``chappie/ui/tray.py`` — no platform marker,
renders ``ChappieState`` icons via PIL). This satisfies AD-11's "guarantee *some*
presence everywhere" floor: the user still gets IDLE / LISTENING / THINKING /
SPEAKING colour feedback through the tray icon.

``set_state(state)`` maps the orb's coarse lifecycle state onto the tray's
``ChappieState`` enum (``chappie/ui/tray.py``) so the colour vocabulary
(``_STATE_COLORS``) lights up the right hue. The surface never raises and is
idempotent (AD-6).

Import-cleanliness contract (HN-7): ``pystray`` / PIL are only imported lazily by
the tray itself; this module imports ``ChappieState`` from ``chappie.ui.tray``,
which does not import ``pystray`` at module scope (the tray lazy-imports it in
``_run``), so this module stays import-clean on a headless box.
"""

from __future__ import annotations

import logging
from typing import Any

from chappie.ui.tray import ChappieState

log = logging.getLogger(__name__)


# Orb lifecycle state (string) → tray ``ChappieState``. Unknown states fall back
# to IDLE so the tray always shows a defined colour.
_ORB_STATE_TO_CHAPPIE_STATE: dict[str, ChappieState] = {
    "idle": ChappieState.IDLE,
    "listening": ChappieState.LISTENING,
    "thinking": ChappieState.THINKING,
    "speaking": ChappieState.SPEAKING,
    "error": ChappieState.ERROR,
    "paused": ChappieState.PAUSED,
}


class TrayOnlySurface:
    """Drive the pystray tray as the overlay floor (:class:`OverlaySurface`).

    A tray can be injected (``tray=``) so tests assert the orb-state → tray-state
    mapping against a fake without spinning up a real pystray thread.
    """

    def __init__(self, *, tray: Any = None) -> None:
        self._tray = tray
        self._owns_tray = tray is None
        self._started = False
        self._state = "idle"

    def _ensure_tray(self) -> Any:
        """Lazily construct ``ChappieTray`` (the import of which is cheap; pystray
        itself is lazy inside the tray's own ``_run``)."""
        if self._tray is None:
            from chappie.ui.tray import ChappieTray

            self._tray = ChappieTray()
        return self._tray

    def start(self) -> None:
        if self._started:
            return
        try:
            tray = self._ensure_tray()
            # Only own the tray lifecycle when we created it; an injected tray is
            # the caller's to start/stop.
            if self._owns_tray:
                tray.start()
            self._started = True
            # Reflect the current state once the tray is up.
            self.set_state(self._state)
        except Exception:  # noqa: BLE001 — AD-6: tray start must never crash boot.
            log.exception(
                "TrayOnlySurface: tray start failed; no tray presence this "
                "session (the rest of Chappie is unaffected)."
            )

    def stop(self) -> None:
        tray = self._tray
        self._started = False
        if tray is None or not self._owns_tray:
            return
        try:
            tray.stop()
        except Exception:  # noqa: BLE001
            log.debug("TrayOnlySurface.stop: tray stop failed", exc_info=True)

    def set_state(self, state: str) -> None:
        self._state = state
        tray = self._tray
        if tray is None:
            return
        chappie_state = _ORB_STATE_TO_CHAPPIE_STATE.get(state, ChappieState.IDLE)
        try:
            tray.set_state(chappie_state)
        except Exception:  # noqa: BLE001
            log.debug("TrayOnlySurface.set_state failed", exc_info=True)

    def is_visible(self) -> bool:
        """The tray icon is always present once started — it is the floor."""
        return self._started


__all__ = ["TrayOnlySurface"]
