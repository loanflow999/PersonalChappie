"""Review pipeline (Phase 8.1+).

Data structures, deterministic validators, and loop skeleton for the
quality-gate pipeline. Plan reference: CHAPPIE_REVIEW_AGENT_PLAN.md §6.1
(Phase 8.1 Foundation), §6.2 (Phase 8.2 Skeleton). Real worker and
reviewer spawns are added in Phase 8.3 (`spawns.py`).
"""
from chappie.core.review.audit import (
    AuditPhase,
    AuditRecord,
    AuditStatus,
    ReviewAudit,
)
from chappie.core.review.checks import (
    Check,
    CheckResult,
    PostCheckRunner,
    PreCheckRunner,
    RunnerResult,
    make_output_budget_check,
    no_stub_code,
    output_not_empty,
    task_not_empty,
    valid_json,
)
from chappie.core.review.errors import (
    CapFiredError,
    PipelineError,
    PreCheckFailure,
    ReviewerUnavailable,
    ReviewPipelineError,
    VerdictParseError,
    WorkerSpawnError,
)
from chappie.core.review.io import RunDirectory
from chappie.core.review.pipeline import (
    HARD_CEILING_MAX_ITERATIONS,
    ReviewerSpawn,
    ReviewPipeline,
    WorkerSpawn,
)
from chappie.core.review.policy import PolicyDecision, ReviewPolicy
from chappie.core.review.prompts import (
    build_feedback_block,
    build_reviewer_prompt,
    build_worker_prompt,
    get_rubric_items,
)
from chappie.core.review.spawns import (
    DEFAULT_REVIEWER_BUDGET_USD,
    DEFAULT_REVIEWER_TOOLS,
    DEFAULT_WORKER_BUDGET_USD,
    DEFAULT_WORKER_TOOLS,
    ReviewerSpawner,
    WorkerSpawner,
)
from chappie.core.review.state import (
    IterationRecord,
    PipelineOutcome,
    PipelineResult,
    RunState,
)
from chappie.core.review.verdict import (
    ReviewIssue,
    ReviewStatus,
    ReviewVerdict,
    RubricResult,
)

__all__ = [
    # verdict
    "ReviewStatus",
    "ReviewIssue",
    "RubricResult",
    "ReviewVerdict",
    # checks
    "Check",
    "CheckResult",
    "RunnerResult",
    "PreCheckRunner",
    "PostCheckRunner",
    "task_not_empty",
    "output_not_empty",
    "make_output_budget_check",
    "no_stub_code",
    "valid_json",
    # audit
    "AuditPhase",
    "AuditStatus",
    "AuditRecord",
    "ReviewAudit",
    # errors
    "ReviewPipelineError",
    "PipelineError",
    "PreCheckFailure",
    "VerdictParseError",
    "CapFiredError",
    "ReviewerUnavailable",
    "WorkerSpawnError",
    # state
    "RunState",
    "IterationRecord",
    "PipelineResult",
    "PipelineOutcome",
    # pipeline
    "ReviewPipeline",
    "WorkerSpawn",
    "ReviewerSpawn",
    "HARD_CEILING_MAX_ITERATIONS",
    # policy
    "ReviewPolicy",
    "PolicyDecision",
    # io
    "RunDirectory",
    # prompts
    "build_feedback_block",
    "build_worker_prompt",
    "build_reviewer_prompt",
    "get_rubric_items",
    # spawns
    "WorkerSpawner",
    "ReviewerSpawner",
    "DEFAULT_WORKER_TOOLS",
    "DEFAULT_REVIEWER_TOOLS",
    "DEFAULT_WORKER_BUDGET_USD",
    "DEFAULT_REVIEWER_BUDGET_USD",
]
