"""Artifacts — the self-contained pages Chappie builds when asked for one.

An artifact is ONE HTML file a person looks at: a dashboard, a report, an
infographic, a small interactive tool. It is authored by a mission worker on
the strongest model the install has (the same sub-agent path ``spawn_worker``
uses), not by the router brain, and it lands in the run archive like every
other deliverable — so the Outputs surfaces, the Downloads mirror and the
Artifacts section all see it without a second store.

Two pieces live here:

* :mod:`~chappie.artifacts.brief` — the worker's task instruction: what a
  finished artifact is (one file, inline assets, no network, brand look), plus
  the previous version when a revision is asked for.
* :mod:`~chappie.artifacts.locate` — find an existing artifact in the archive
  by title, so "make the bars red" can start from the page it refers to.

The tool that dispatches the mission is ``chappie.plugins.tool.create_artifact``;
the gate that decides whether the tool is offered on a turn at all is
``chappie.brain.artifact_gate`` — ask-only, never ambient.
"""

from __future__ import annotations

from chappie.artifacts.brief import (
    MAX_PREVIOUS_HTML_CHARS,
    ArtifactBrief,
    artifact_filename,
    build_artifact_brief,
)
from chappie.artifacts.locate import LocatedArtifact, locate_artifact

__all__ = [
    "MAX_PREVIOUS_HTML_CHARS",
    "ArtifactBrief",
    "LocatedArtifact",
    "artifact_filename",
    "build_artifact_brief",
    "locate_artifact",
]
