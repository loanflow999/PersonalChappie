"""Portable persistence tests for the user-managed MCP registry."""

from __future__ import annotations

import json

from chappie.mcp import state


def test_chappie_data_dir_owns_mcp_config_on_headless_hosts(
    monkeypatch,
    tmp_path,
) -> None:
    data_dir = tmp_path / "mounted-data"
    legacy_project = tmp_path / "read-only-app" / "mcp.json"
    monkeypatch.setenv("CHAPPIE_DATA_DIR", str(data_dir))
    monkeypatch.delenv("CHAPPIE_MCP_CONFIG", raising=False)
    monkeypatch.setattr(state, "MCP_JSON_PATH", legacy_project)

    state.save_config({"mcpServers": {"remote": {"enabled": True}}})

    assert not legacy_project.exists()
    assert json.loads((data_dir / "mcp.json").read_text(encoding="utf-8")) == {
        "mcpServers": {"remote": {"enabled": True}}
    }
    assert state.load_config()["mcpServers"]["remote"]["enabled"] is True


def test_unwritable_project_config_crosses_to_per_user_storage(
    monkeypatch,
    tmp_path,
) -> None:
    blocked_parent = tmp_path / "not-a-directory"
    blocked_parent.write_text("blocked", encoding="utf-8")
    monkeypatch.delenv("CHAPPIE_DATA_DIR", raising=False)
    monkeypatch.delenv("CHAPPIE_MCP_CONFIG", raising=False)
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "user-data"))
    monkeypatch.setattr(state, "MCP_JSON_PATH", blocked_parent / "mcp.json")

    state.save_config({"mcpServers": {"hosted": {"enabled": True}}})

    fallback = tmp_path / "user-data" / "Chappie" / "mcp.json"
    assert fallback.exists()
    assert state.load_config()["mcpServers"]["hosted"]["enabled"] is True


def test_explicit_mcp_config_path_is_not_silently_redirected(
    monkeypatch,
    tmp_path,
) -> None:
    explicit = tmp_path / "custom" / "servers.json"
    monkeypatch.setenv("CHAPPIE_MCP_CONFIG", str(explicit))
    monkeypatch.setenv("CHAPPIE_DATA_DIR", str(tmp_path / "data"))

    state.save_config({"mcpServers": {}})

    assert explicit.exists()
    assert not (tmp_path / "data" / "mcp.json").exists()
