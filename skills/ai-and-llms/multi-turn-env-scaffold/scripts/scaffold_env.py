#!/usr/bin/env python3
"""Scaffold a reproducible multi-turn RL environment and stratified task dataset.

Implements the workflows from `multi-turn-env-scaffold`:
- Immutable Task Dataset generation with stratified difficulty buckets
- Isolated per-episode state reset (`reset()`)
- State-conditioned deterministic per-turn seeding (`derive_turn_seed()`)
- Soft invalid-action penalty (`-0.1`) with continuation up to `max_turns`
- Unbiased randomized tie-breaking seeded by the state-turn hash
- Built-in verification suite producing `scaffold_check_report.json`
"""

from __future__ import annotations
import argparse
import copy
import hashlib
import json
import random
import re
from pathlib import Path
from typing import Any


def derive_turn_seed(example_seed: int, state_snapshot: dict[str, Any], turn: int) -> int:
    payload = json.dumps(
        {"seed": example_seed, "state": state_snapshot, "turn": turn},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return int(hashlib.sha256(payload).hexdigest()[:16], 16)


ENV_CORE_SOURCE = '''#!/usr/bin/env python3
"""Generated Multi-Turn RL Environment Core (`env_core.py`).

Domain: Stateful Grid-World & Bug-Repair Gym with deterministic turn seeding,
soft invalid-action penalties, and isolated episode resets.
"""

from __future__ import annotations
import copy
import hashlib
import json
import random
import re
from typing import Any

ACTION_RE = re.compile(r"<action>\\s*([^<]+?)\\s*</action>", re.IGNORECASE)
THINK_RE = re.compile(r"<think>.*?</think>", re.IGNORECASE | re.DOTALL)


def derive_turn_seed(example_seed: int, canonical_state: dict[str, Any], turn: int) -> int:
    payload = json.dumps(
        {"seed": example_seed, "state": canonical_state, "turn": turn},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return int(hashlib.sha256(payload).hexdigest()[:16], 16)


class ReproducibleGridRepairEnv:
    """Multi-turn environment where an agent navigates a 4x4 diagnostic grid
    to inspect and patch a faulty node while avoiding hazards.
    """

    VALID_ACTIONS = ("UP", "DOWN", "LEFT", "RIGHT", "INSPECT", "PATCH")

    def __init__(self, max_turns: int = 8, invalid_penalty: float = -0.10) -> None:
        self.max_turns = max_turns
        self.invalid_penalty = invalid_penalty
        self._state: dict[str, Any] = {}

    def reset(self, task_row: dict[str, Any]) -> dict[str, Any]:
        """Initialize an isolated episode state from an immutable task dataset row."""
        row = copy.deepcopy(task_row)
        gt = row["ground_truth"]
        self._state = {
            "task_id": row["task_id"],
            "example_seed": int(row["example_seed"]),
            "difficulty_bucket": row["difficulty_bucket"],
            "hazard_drift_prob": float(row["stochastic_prob"]),
            "grid_size": int(gt.get("grid_size", 4)),
            "agent_pos": list(gt["start_pos"]),
            "target_pos": list(gt["target_pos"]),
            "hazards": [list(h) for h in gt["hazards"]],
            "bug_code": str(gt["bug_code"]),
            "inspected": False,
            "patched": False,
            "turn": 0,
            "max_turns": self.max_turns,
            "invalid_moves": 0,
            "format_hits": 0,
            "step_Penalty_accum": 0.0,
            "terminated": False,
            "termination_reason": None,
            "winner": False,
        }
        return self._build_observation("Episode initialized. Navigate to target, INSPECT, then PATCH.")

    def get_state_copy(self) -> dict[str, Any]:
        return copy.deepcopy(self._state)

    def _canonical_board_state(self) -> dict[str, Any]:
        return {
            "agent_pos": self._state["agent_pos"],
            "target_pos": self._state["target_pos"],
            "hazards": sorted(self._state["hazards"]),
            "inspected": self._state["inspected"],
            "patched": self._state["patched"],
        }

    def _build_observation(self, message: str) -> dict[str, Any]:
        return {
            "observation_text": (
                f"[Turn {self._state['turn']}/{self._state['max_turns']}] {message} | "
                f"pos={tuple(self._state['agent_pos'])}, target={tuple(self._state['target_pos'])}, "
                f"hazards={[tuple(h) for h in self._state['hazards']]}, "
                f"inspected={self._state['inspected']}, patched={self._state['patched']}. "
                "Respond with <think>...</think><action>UP|DOWN|LEFT|RIGHT|INSPECT|PATCH</action>."
            ),
            "state": self.get_state_copy(),
            "terminated": bool(self._state["terminated"]),
        }

    def step(self, raw_completion: str) -> dict[str, Any]:
        """Process one agent response, apply soft penalties on invalid moves, and update state."""
        if self._state.get("terminated"):
            raise RuntimeError("Cannot call step() on a terminated episode; call reset() first.")

        self._state["turn"] += 1
        turn = self._state["turn"]
        has_think = bool(THINK_RE.search(raw_completion or ""))
        match = ACTION_RE.search(raw_completion or "")

        step_reward = 0.0
        if not match:
            self._state["invalid_moves"] += 1
            step_reward += self.invalid_penalty
            self._state["step_Penalty_accum"] = round(self._state["step_Penalty_accum"] + self.invalid_penalty, 4)
            feedback = "Invalid format: missing <action>...</action> tag. Soft penalty applied."
        else:
            action = match.group(1).strip().upper()
            if has_think:
                self._state["format_hits"] += 1
            if action not in self.VALID_ACTIONS:
                self._state["invalid_moves"] += 1
                step_reward += self.invalid_penalty
                self._state["step_Penalty_accum"] = round(self._state["step_Penalty_accum"] + self.invalid_penalty, 4)
                feedback = f"Unknown action '{action}'. Valid actions: {self.VALID_ACTIONS}."
            else:
                feedback, delta_r = self._apply_valid_action(action)
                step_reward += delta_r

        # Deterministic environment transition (hazard drift) seeded by (example_seed, state, turn)
        turn_seed = derive_turn_seed(
            self._state["example_seed"],
            self._canonical_board_state(),
            turn,
        )
        rng = random.Random(turn_seed)
        if not self._state["terminated"] and rng.random() < self._state["hazard_drift_prob"]:
            self._drift_hazard_unbiased(rng)

        if self._state["patched"]:
            self._state["terminated"] = True
            self._state["termination_reason"] = "goal_reached"
            self._state["winner"] = True
        elif self._state["turn"] >= self._state["max_turns"]:
            self._state["terminated"] = True
            self._state["termination_reason"] = "max_turns_reached"

        obs = self._build_observation(feedback)
        obs["step_reward"] = round(step_reward, 4)
        obs["turn_seed"] = turn_seed
        return obs

    def _apply_valid_action(self, action: str) -> tuple[str, float]:
        r, c = self._state["agent_pos"]
        g = self._state["grid_size"]
        if action in ("UP", "DOWN", "LEFT", "RIGHT"):
            nr, nc = r, c
            if action == "UP":
                nr = max(0, r - 1)
            elif action == "DOWN":
                nr = min(g - 1, r + 1)
            elif action == "LEFT":
                nc = max(0, c - 1)
            elif action == "RIGHT":
                nc = min(g - 1, c + 1)
            if [nr, nc] == [r, c]:
                self._state["invalid_moves"] += 1
                self._state["step_Penalty_accum"] = round(self._state["step_Penalty_accum"] + self.invalid_penalty, 4)
                return ("Blocked by grid boundary; position unchanged.", self.invalid_penalty)
            if [nr, nc] in self._state["hazards"]:
                self._state["invalid_moves"] += 1
                self._state["step_Penalty_accum"] = round(self._state["step_Penalty_accum"] + self.invalid_penalty, 4)
                return (f"Collision with hazard at {(nr, nc)}; position unchanged.", self.invalid_penalty)
            self._state["agent_pos"] = [nr, nc]
            return (f"Moved {action} to {(nr, nc)}.", 0.0)

        if action == "INSPECT":
            if self._state["agent_pos"] == self._state["target_pos"]:
                self._state["inspected"] = True
                return (f"Inspected faulty node: bug_code={self._state['bug_code']}.", 0.20)
            self._state["invalid_moves"] += 1
            self._state["step_Penalty_accum"] = round(self._state["step_Penalty_accum"] + self.invalid_penalty, 4)
            return ("Cannot INSPECT: not standing on target_pos.", self.invalid_penalty)

        if action == "PATCH":
            if self._state["agent_pos"] == self._state["target_pos"] and self._state["inspected"]:
                self._state["patched"] = True
                return ("Patch applied successfully! Target node verified.", 1.00)
            self._state["invalid_moves"] += 1
            self._state["step_Penalty_accum"] = round(self._state["step_Penalty_accum"] + self.invalid_penalty, 4)
            return ("Cannot PATCH before reaching target_pos and running INSPECT.", self.invalid_penalty)

        return ("No-op.", 0.0)

    def _drift_hazard_unbiased(self, rng: random.Random) -> None:
        """Unbiased tie-breaking using state-seeded RNG rather than first-index selection."""
        if not self._state["hazards"]:
            return
        g = self._state["grid_size"]
        h_idx = rng.randrange(len(self._state["hazards"]))
        hr, hc = self._state["hazards"][h_idx]
        candidates = []
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = hr + dr, hc + dc
            if 0 <= nr < g and 0 <= nc < g:
                if [nr, nc] != self._state["agent_pos"] and [nr, nc] != self._state["target_pos"]:
                    if [nr, nc] not in self._state["hazards"]:
                        candidates.append([nr, nc])
        if candidates:
            # Random tie-breaking across valid candidate cells prevents trajectory memorization
            self._state["hazards"][h_idx] = rng.choice(candidates)
'''


def generate_stratified_dataset(num_tasks: int, min_prob: float, max_prob: float) -> list[dict[str, Any]]:
    strata = [
        ("easy", round(min_prob, 3)),
        ("medium", round((min_prob + max_prob) / 2.0, 3)),
        ("hard", round(max_prob, 3)),
    ]
    rows: list[dict[str, Any]] = []
    for idx in range(num_tasks):
        bucket_name, prob = strata[idx % len(strata)]
        seed = 1000 + idx * 17
        rng = random.Random(seed)
        target_r = rng.choice([1, 2, 3])
        target_c = rng.choice([1, 2, 3])
        hazard_candidates = [
            [r, c]
            for r in range(4)
            for c in range(4)
            if [r, c] not in ([0, 0], [target_r, target_c])
        ]
        hazards = rng.sample(hazard_candidates, k=2)
        rows.append(
            {
                "artifact_type": "task_dataset",
                "task_id": f"grid-repair-{idx:03d}",
                "example_seed": seed,
                "difficulty_bucket": bucket_name,
                "stochastic_prob": prob,
                "initial_prompt": (
                    f"Task grid-repair-{idx:03d}: Start at (0, 0) on a 4x4 grid. "
                    f"Navigate to target ({target_r}, {target_c}) avoiding hazards {hazards}, "
                    "execute INSPECT, then execute PATCH. Wrap thoughts in <think>...</think> "
                    "and your command in <action>...</action>."
                ),
                "ground_truth": {
                    "grid_size": 4,
                    "start_pos": [0, 0],
                    "target_pos": [target_r, target_c],
                    "hazards": hazards,
                    "bug_code": f"ERR_OFFSET_{seed % 97:02d}",
                },
            }
        )
    return rows


def run_self_checks(env_dir: Path, dataset: list[dict[str, Any]]) -> dict[str, Any]:
    import importlib.util
    spec = importlib.util.spec_from_file_location("env_core", env_dir / "env_core.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    env_a = mod.ReproducibleGridRepairEnv(max_turns=8, invalid_penalty=-0.10)
    env_b = mod.ReproducibleGridRepairEnv(max_turns=8, invalid_penalty=-0.10)

    sample_row = dataset[0]
    obs_a0 = env_a.reset(sample_row)
    obs_b0 = env_b.reset(sample_row)

    scripted_actions = [
        "<think>Move right</think><action>RIGHT</action>",
        "malformed response without tags",
        "<think>Move down</think><action>DOWN</action>",
    ]
    trace_a, trace_b = [], []
    for act in scripted_actions:
        trace_a.append(env_a.step(act))
        trace_b.append(env_b.step(act))

    determinism_passed = (
        json.dumps(trace_a, sort_keys=True) == json.dumps(trace_b, sort_keys=True)
    )
    soft_penalty_passed = (
        trace_a[1]["terminated"] is False
        and trace_a[1]["step_reward"] == -0.10
        and trace_a[1]["state"]["invalid_moves"] >= 1
    )

    # Check reset isolation
    obs_a_reset = env_a.reset(sample_row)
    reset_isolation_passed = (
        json.dumps(obs_a0["state"], sort_keys=True)
        == json.dumps(obs_a_reset["state"], sort_keys=True)
    )

    counts: dict[str, int] = {}
    for row in dataset:
        b = row["difficulty_bucket"]
        counts[b] = counts.get(b, 0) + 1
    stratification_passed = len(set(counts.values())) == 1

    return {
        "env_name": env_dir.name,
        "num_tasks": len(dataset),
        "bucket_counts": counts,
        "determinism_check_passed": determinism_passed,
        "soft_invalid_action_continuation_passed": soft_penalty_passed,
        "reset_isolation_passed": reset_isolation_passed,
        "stratification_balance_passed": stratification_passed,
        "all_checks_passed": bool(
            determinism_passed
            and soft_penalty_passed
            and reset_isolation_passed
            and stratification_passed
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a reproducible multi-turn RL environment.")
    parser.add_argument("--env-name", default="grid-repair-env", help="Environment folder name")
    parser.add_argument("--output-dir", default="rl-env-skills/examples", help="Parent output directory")
    parser.add_argument("--num-tasks", type=int, default=12, help="Number of tasks (multiple of 3)")
    parser.add_argument("--min-prob", type=float, default=0.0, help="Min hazard drift probability")
    parser.add_argument("--max-prob", type=float, default=0.5, help="Max hazard drift probability")
    args = parser.parse_args()

    env_dir = Path(args.output_dir) / args.env_name
    env_dir.mkdir(parents=True, exist_ok=True)

    (env_dir / "env_core.py").write_text(ENV_CORE_SOURCE, encoding="utf-8")

    template_src = Path(__file__).resolve().parent.parent / "templates" / "verifiers_v1_taskset_template.py"
    if template_src.exists():
        (env_dir / "verifiers_v1_taskset.py").write_text(
            template_src.read_text(encoding="utf-8"), encoding="utf-8"
        )

    dataset = generate_stratified_dataset(args.num_tasks, args.min_prob, args.max_prob)
    ds_path = env_dir / "tasks_dataset.jsonl"
    with ds_path.open("w", encoding="utf-8") as f:
        for row in dataset:
            f.write(json.dumps(row) + "\n")

    report = run_self_checks(env_dir, dataset)
    report_path = env_dir / "scaffold_check_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
