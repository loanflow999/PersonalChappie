"""Back-compat tests for the 2026-06-29 Chappie-Agents config-key rename.

Verifies that existing installs whose chappie.toml / env-vars still use the OLD
key names ([brain.sub_chappie], [harness.openclaw], [sub_agents]) continue to
populate the new fields (brain.worker, harness.chappie_agent, chappie_agents)
after the rename.  Also verifies that the NEW key names work.

These tests do NOT touch the real chappie.toml on disk.
"""
from __future__ import annotations

import os

import pytest

from chappie.core.config import BrainConfig, HarnessConfig, ChappieConfig


# ---------------------------------------------------------------------------
# 6a — [sub_agents] → [chappie_agents]
# ---------------------------------------------------------------------------


def test_chappie_agents_populated_from_old_sub_agents_key() -> None:
    """Old [sub_agents] TOML key populates the new chappie_agents field."""
    cfg = ChappieConfig(**{"sub_agents": {"output_dir": "old-path"}})
    assert cfg.chappie_agents is not None


def test_chappie_agents_populated_from_new_key() -> None:
    """New [chappie_agents] TOML key populates chappie_agents field."""
    cfg = ChappieConfig(**{"chappie_agents": {"output_dir": "new-path"}})
    assert cfg.chappie_agents is not None


def test_chappie_agents_default_when_absent() -> None:
    """Absent [chappie_agents] / [sub_agents] block yields the default."""
    cfg = ChappieConfig()
    assert cfg.chappie_agents is not None  # default_factory


# ---------------------------------------------------------------------------
# 6b — [harness.openclaw] → [harness.chappie_agent]
# ---------------------------------------------------------------------------


def test_harness_chappie_agent_from_old_openclaw_key() -> None:
    """Old [harness.openclaw] TOML key populates the new chappie_agent field."""
    cfg = HarnessConfig(**{"openclaw": {"version": "1.0.0", "enabled": True}})
    assert cfg.chappie_agent is not None
    assert cfg.chappie_agent.version == "1.0.0"
    assert cfg.chappie_agent.enabled is True


def test_harness_chappie_agent_from_new_key() -> None:
    """New [harness.chappie_agent] TOML key populates chappie_agent field."""
    cfg = HarnessConfig(**{"chappie_agent": {"version": "2.0.0", "enabled": False}})
    assert cfg.chappie_agent is not None
    assert cfg.chappie_agent.version == "2.0.0"


def test_harness_chappie_agent_none_when_absent() -> None:
    """Absent harness block leaves chappie_agent as None."""
    cfg = HarnessConfig()
    assert cfg.chappie_agent is None


# ---------------------------------------------------------------------------
# 6c — [brain.sub_chappie] → [brain.worker]   (highest risk)
# ---------------------------------------------------------------------------


def test_brain_worker_from_old_sub_chappie_key() -> None:
    """Old [brain.sub_chappie] TOML key populates the new brain.worker field."""
    cfg = BrainConfig(
        **{"sub_chappie": {"provider": "antigravity", "model": "claude-opus-4-8"}}
    )
    assert cfg.worker is not None
    assert cfg.worker.provider == "antigravity"
    assert cfg.worker.model == "claude-opus-4-8"


def test_brain_worker_from_new_key() -> None:
    """New [brain.worker] TOML key populates brain.worker field."""
    cfg = BrainConfig(
        **{"worker": {"provider": "gemini", "model": "gemini-3.5-flash"}}
    )
    assert cfg.worker is not None
    assert cfg.worker.provider == "gemini"
    assert cfg.worker.model == "gemini-3.5-flash"


def test_brain_worker_none_when_absent() -> None:
    """Absent [brain.worker] / [brain.sub_chappie] block leaves worker as None."""
    cfg = BrainConfig()
    assert cfg.worker is None


def test_brain_worker_fallback_chain_preserved() -> None:
    """Fallback fields on the old block come through intact."""
    cfg = BrainConfig(
        **{
            "sub_chappie": {
                "provider": "antigravity",
                "model": "claude-opus-4-8",
                "fallback_provider": "gemini",
                "fallback_model": "gemini-3.1-pro-preview",
            }
        }
    )
    assert cfg.worker is not None
    assert cfg.worker.fallback_provider == "gemini"
    assert cfg.worker.fallback_model == "gemini-3.1-pro-preview"


# ---------------------------------------------------------------------------
# Full round-trip via ChappieConfig (as load_config constructs it)
# ---------------------------------------------------------------------------


def test_full_config_old_keys_round_trip() -> None:
    """ChappieConfig(**raw_dict_with_old_keys) populates all three renamed fields."""
    raw = {
        "brain": {
            "sub_chappie": {
                "provider": "antigravity",
                "model": "claude-opus-4-8",
            }
        },
        "harness": {
            "openclaw": {
                "version": "1.0.0",
                "enabled": False,
            }
        },
        "sub_agents": {},
    }
    cfg = ChappieConfig(**raw)

    # brain.worker (was brain.sub_chappie)
    assert cfg.brain.worker is not None
    assert cfg.brain.worker.provider == "antigravity"
    assert cfg.brain.worker.model == "claude-opus-4-8"

    # harness.chappie_agent (was harness.openclaw)
    assert cfg.harness.chappie_agent is not None
    assert cfg.harness.chappie_agent.version == "1.0.0"

    # chappie_agents (was sub_agents)
    assert cfg.chappie_agents is not None


def test_full_config_new_keys_round_trip() -> None:
    """ChappieConfig(**raw_dict_with_new_keys) also populates all three fields."""
    raw = {
        "brain": {
            "worker": {
                "provider": "gemini",
                "model": "gemini-3.5-flash",
            }
        },
        "harness": {
            "chappie_agent": {
                "version": "2.0.0",
                "enabled": False,
            }
        },
        "chappie_agents": {},
    }
    cfg = ChappieConfig(**raw)

    assert cfg.brain.worker is not None
    assert cfg.brain.worker.provider == "gemini"

    assert cfg.harness.chappie_agent is not None
    assert cfg.harness.chappie_agent.version == "2.0.0"

    assert cfg.chappie_agents is not None


# ---------------------------------------------------------------------------
# ENV migration shim (_migrate_worker_env_vars)
# ---------------------------------------------------------------------------


def test_migrate_worker_env_vars_copies_old_to_new(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Old CHAPPIE__BRAIN__SUB_CHAPPIE__PROVIDER is copied to the new name."""
    from chappie.core.config import _migrate_worker_env_vars

    monkeypatch.setenv("CHAPPIE__BRAIN__SUB_CHAPPIE__PROVIDER", "antigravity")
    monkeypatch.delenv("CHAPPIE__BRAIN__WORKER__PROVIDER", raising=False)

    _migrate_worker_env_vars()

    assert os.environ["CHAPPIE__BRAIN__WORKER__PROVIDER"] == "antigravity"


def test_migrate_worker_env_vars_does_not_overwrite_new(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Does not overwrite CHAPPIE__BRAIN__WORKER__PROVIDER if already set."""
    from chappie.core.config import _migrate_worker_env_vars

    monkeypatch.setenv("CHAPPIE__BRAIN__SUB_CHAPPIE__PROVIDER", "old-value")
    monkeypatch.setenv("CHAPPIE__BRAIN__WORKER__PROVIDER", "gemini")

    _migrate_worker_env_vars()

    assert os.environ["CHAPPIE__BRAIN__WORKER__PROVIDER"] == "gemini"  # unchanged


def test_migrate_worker_env_vars_noop_when_old_absent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No-op when neither old nor new is set."""
    from chappie.core.config import _migrate_worker_env_vars

    monkeypatch.delenv("CHAPPIE__BRAIN__SUB_CHAPPIE__PROVIDER", raising=False)
    monkeypatch.delenv("CHAPPIE__BRAIN__WORKER__PROVIDER", raising=False)

    _migrate_worker_env_vars()  # must not raise

    assert "CHAPPIE__BRAIN__WORKER__PROVIDER" not in os.environ
