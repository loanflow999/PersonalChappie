"""Contract tests for the OpenAI, Gemini and Deepgram cloud STT plugins.

New STT providers MUST pass ``tests/contract/``. These assert the two plugins
added to close the single-key STT gap (an OpenAI-only or Gemini-only downloader
had no cloud speech-to-text) satisfy the ``STTProvider`` structural contract:

  * ``name`` matches the ``chappie.stt`` entry-point id,
  * ``supports_streaming`` exists and ``transcribe`` / ``stream_transcribe`` /
    ``transcribe_pcm`` have the right async shapes,
  * a constructed instance is a runtime ``STTProvider``,
  * the plugin module imports NO ``chappie.*`` at module load time (entry-point
    plugins stay import-clean; the credential lookup may import lazily inside a
    method, mirroring the OpenRouter STT plugin).

The classes are imported directly (not via entry-point discovery) so the file is
green regardless of whether ``pip install -e .`` has re-registered the new
entry-points yet.
"""
from __future__ import annotations

import importlib
import inspect
from pathlib import Path

import pytest

from chappie.core.protocols import STTProvider
from chappie.plugins.stt.deepgram_api import DeepgramSTT
from chappie.plugins.stt.gemini_api import GeminiSTT
from chappie.plugins.stt.openai_api import OpenAIWhisperAPI

_CASES = [
    ("openai-api", OpenAIWhisperAPI, "chappie.plugins.stt.openai_api"),
    ("gemini-api", GeminiSTT, "chappie.plugins.stt.gemini_api"),
    ("deepgram-api", DeepgramSTT, "chappie.plugins.stt.deepgram_api"),
]


@pytest.mark.parametrize("name,cls,_mod", _CASES)
def test_class_name_matches_entry_point(name, cls, _mod) -> None:
    assert cls.name == name, f"{cls.__name__}.name = {cls.name!r}, expected {name!r}"


@pytest.mark.parametrize("name,cls,_mod", _CASES)
def test_provider_has_required_shapes(name, cls, _mod) -> None:
    assert hasattr(cls, "supports_streaming")
    assert inspect.iscoroutinefunction(cls.transcribe)
    assert inspect.isasyncgenfunction(cls.stream_transcribe)
    assert inspect.iscoroutinefunction(cls.transcribe_pcm)


def test_openai_instance_is_stt_provider() -> None:
    assert isinstance(OpenAIWhisperAPI(api_key="dummy"), STTProvider)


def test_gemini_instance_is_stt_provider() -> None:
    assert isinstance(GeminiSTT(api_key="dummy"), STTProvider)


def test_deepgram_instance_is_stt_provider() -> None:
    assert isinstance(DeepgramSTT(api_key="dummy"), STTProvider)


@pytest.mark.parametrize("name,_cls,mod_name", _CASES)
def test_plugin_module_has_no_top_level_chappie_import(name, _cls, mod_name) -> None:
    """No ``chappie.*`` import at MODULE level (column 0). A lazy import inside a
    method is allowed — the OpenRouter STT plugin does the same for its
    credential lookup."""
    mod = importlib.import_module(mod_name)
    source = Path(mod.__file__).read_text(encoding="utf-8")
    offending = [
        ln
        for ln in source.splitlines()
        # Only flag top-level (unindented) import statements.
        if ln[:1] not in (" ", "\t")
        and ln.startswith(("from chappie", "import chappie"))
    ]
    assert not offending, (
        f"top-level chappie.* imports leaked into {mod_name}: " + "; ".join(offending)
    )
