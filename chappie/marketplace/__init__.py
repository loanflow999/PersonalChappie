"""Plugin Marketplace — connect Personal Chappie to third-party services."""

from chappie.marketplace.auth.base import (
    AuthHandler,
    AuthSession,
    FlowRegistry,
    FlowResult,
    get_registry,
    pkce_pair,
)
from chappie.marketplace.auth.oauth_dcr import DcrConfig, HostedMcpDcrHandler
from chappie.marketplace.catalog import (
    AuthConfig,
    HostedMcpAllowlistAuth,
    HostedMcpOAuthDcrAuth,
    OAuthDeviceFlowAuth,
    OAuthPkceLoopbackAuth,
    PatPasteAuth,
    PluginCatalog,
    PluginSpec,
)
from chappie.marketplace.catalog_data import clear_cache, load_catalog
from chappie.marketplace.oauth_callback_server import (
    CallbackResult,
    CallbackTimeoutError,
    OAuthCallbackServer,
)
from chappie.marketplace.token_store import (
    InMemoryBackend,
    KeyringBackend,
    TokenBackend,
    Tokens,
    TokenStore,
)

__all__ = [
    "AuthConfig",
    "AuthHandler",
    "AuthSession",
    "CallbackResult",
    "CallbackTimeoutError",
    "DcrConfig",
    "FlowRegistry",
    "FlowResult",
    "HostedMcpAllowlistAuth",
    "HostedMcpDcrHandler",
    "HostedMcpOAuthDcrAuth",
    "InMemoryBackend",
    "KeyringBackend",
    "OAuthCallbackServer",
    "OAuthDeviceFlowAuth",
    "OAuthPkceLoopbackAuth",
    "PatPasteAuth",
    "PluginCatalog",
    "PluginSpec",
    "TokenBackend",
    "Tokens",
    "TokenStore",
    "clear_cache",
    "get_registry",
    "load_catalog",
    "pkce_pair",
]
