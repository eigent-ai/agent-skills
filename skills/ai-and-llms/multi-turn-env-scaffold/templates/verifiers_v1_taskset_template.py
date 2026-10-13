"""Template: Prime Intellect Verifiers v1 Taskset + Stateful Environment Wrapper.

Adapted to verifiers.v1 API (https://docs.primeintellect.ai/verifiers/v1/tasksets.md,
checked 2026-10-12) and multi-turn state/seeding patterns from 71V3fTaUp2Q and V-EDrhIhHzQ.
"""

from __future__ import annotations
import hashlib
import json
import random
from dataclasses import dataclass, field
from typing import Any

# Optional import: runs standalone if verifiers.v1 is not installed
try:
    import verifiers.v1 as vf  # type: ignore
    HAS_VERIFIERS_V1 = True
except ImportError:
    HAS_VERIFIERS_V1 = False


def derive_turn_seed(example_seed: int, canonical_state: dict[str, Any], turn: int) -> int:
    """Derive a deterministic seed from (example_seed, state, turn) for GRPO noise reduction."""
    payload = json.dumps(
        {"seed": example_seed, "state": canonical_state, "turn": turn},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()
    return int(digest[:16], 16)


@dataclass(frozen=True)
class EnvTaskData:
    """Immutable Task Dataset row (distinct from recorded trajectories and SFT examples)."""
    task_id: str
    example_seed: int
    difficulty_bucket: str
    stochastic_prob: float
    initial_prompt: str
    ground_truth: dict[str, Any]
    artifact_type: str = "task_dataset"


@dataclass
class EnvTaskConfig:
    """Configuration shared across tasks in a Taskset."""
    max_turns: int = 8
    invalid_action_penalty: float = -0.10
    format_reward_weight: float = 0.20
    outcome_reward_weight: float = 1.00
    conciseness_bonus_weight: float = 0.10
    extra: dict[str, Any] = field(default_factory=dict)
