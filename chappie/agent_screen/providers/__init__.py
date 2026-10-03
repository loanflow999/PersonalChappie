"""Screen providers, one per way of getting an isolated session on a host."""

from chappie.agent_screen.providers.attached import AttachedProvider
from chappie.agent_screen.providers.windows_sandbox import WindowsSandboxProvider
from chappie.agent_screen.providers.xvfb import XvfbProvider

__all__ = ["AttachedProvider", "WindowsSandboxProvider", "XvfbProvider"]
