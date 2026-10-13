#!/usr/bin/env python3
"""Scaffold and validate a Harbor / Terminal-Bench style sandboxed task package.

Implements `sandboxed-task-packaging`:
1. Generates a complete non-tutorial "make this failing unit test pass" task package
   (`fix-ledger-rounding-bug`) if `--init-example` is passed.
2. Audits directory layout and `task.toml` configuration (`[verifier].environment_mode = "separate"`).
3. Verifies zero leakage of `tests/` and `solution.sh` into the agent-visible `workspace/` or `Dockerfile`.
4. Executes a Null Baseline check in an isolated sandbox (asserting `reward == 0.0`).
5. Executes an Oracle Solution check (`solution.sh`) followed by separate-verifier grading
   (asserting `reward == 1.0` in `logs/verifier/reward.json`).
"""

from __future__ import annotations
import argparse
import json
import os
import shutil
import subprocess
import tempfile
import tomllib
from pathlib import Path
from typing import Any


INSTRUCTION_MD = """# Task: Fix Integer-Cent Ledger Reconciliation (`fix-ledger-rounding-bug`)

## Problem Description
The module `src/ledger.py` implements `reconcile_balances(opening_cents, postings, fee_bps)`.
Currently, two defects cause reconciliation failures:
1. Percentage fees (`fee_bps` in basis points, where `100 bps = 1%`) are truncated with `int()` instead of rounded to the nearest integer cent (`round()`), causing systematic under-collection on odd basis-point fees.
2. Duplicate `tx_id` entries inside `postings` are applied multiple times instead of being deduplicated by keeping only the **first** seen transaction for each `tx_id`.

## Acceptance Criteria
Edit `src/ledger.py` so that `reconcile_balances(opening_cents: int, postings: list[dict], fee_bps: int) -> dict` satisfies:
- Deduplicates `postings` by `tx_id` in arrival order (first occurrence wins).
- For each unique posting with `"amount_cents"`, computes the fee on **debit** transactions (`amount_cents < 0`) as `round(abs(amount_cents) * fee_bps / 10000)`. Credit transactions (`amount_cents >= 0`) incur `0` fee.
- Returns `{"closing_cents": int, "total_fees_cents": int, "applied_tx_ids": list[str]}`.
"""

BUGGY_LEDGER_PY = '''"""Buggy ledger module given to the agent at episode reset."""

from __future__ import annotations
from typing import Any


def reconcile_balances(
    opening_cents: int,
    postings: list[dict[str, Any]],
    fee_bps: int = 25,
) -> dict[str, Any]:
    balance = int(opening_cents)
    total_fees = 0
    applied_ids: list[str] = []

    # BUG 1: Does not deduplicate repeated tx_id entries!
    for item in postings:
        tx_id = str(item["tx_id"])
        amt = int(item["amount_cents"])
        applied_ids.append(tx_id)
        balance += amt
        if amt < 0:
            # BUG 2: Uses floor int() truncation instead of round()
            fee = int((abs(amt) * fee_bps) / 10000)
            balance -= fee
            total_fees += fee

    return {
        "closing_cents": balance,
        "total_fees_cents": total_fees,
        "applied_tx_ids": applied_ids,
    }
'''

DOCKERFILE_TXT = """FROM python:3.11-slim
WORKDIR /app
# Only copy the agent-visible workspace; never copy tests/ or solution.sh
COPY workspace/ /app/
ENV PYTHONUNBUFFERED=1
"""

SOLUTION_SH = """#!/usr/bin/env bash
set -euo pipefail

cat << 'EOF' > src/ledger.py
\"\"\"Repaired ledger module passing all reconciliation invariants.\"\"\"

from __future__ import annotations
from typing import Any


def reconcile_balances(
    opening_cents: int,
    postings: list[dict[str, Any]],
    fee_bps: int = 25,
) -> dict[str, Any]:
    balance = int(opening_cents)
    total_fees = 0
    applied_ids: list[str] = []
    seen: set[str] = set()

    for item in postings:
        tx_id = str(item["tx_id"])
        if tx_id in seen:
            continue
        seen.add(tx_id)
        amt = int(item["amount_cents"])
        applied_ids.append(tx_id)
        balance += amt
        if amt < 0:
            fee = int(round((abs(amt) * fee_bps) / 10000.0))
            balance -= fee
            total_fees += fee

    return {
        "closing_cents": balance,
        "total_fees_cents": total_fees,
        "applied_tx_ids": applied_ids,
    }
EOF
"""

TEST_OUTPUTS_PY = '''"""Held-out verification test suite (`tests/test_outputs.py`)."""

from __future__ import annotations
import importlib.util
import json
import sys
from pathlib import Path


def load_ledger():
    target = Path("src/ledger.py")
    assert target.exists(), "Missing src/ledger.py in grading sandbox"
    spec = importlib.util.spec_from_file_location("ledger", target)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_deduplication_and_rounding():
    mod = load_ledger()
    postings = [
        {"tx_id": "tx-01", "amount_cents": -300},   # fee at 250 bps (2.5%) = round(7.5) = 8 cents
        {"tx_id": "tx-01", "amount_cents": -300},   # duplicate tx_id -> must be ignored
        {"tx_id": "tx-02", "amount_cents": 500},    # credit -> 0 fee
        {"tx_id": "tx-03", "amount_cents": -100},   # fee at 250 bps = round(2.5) = 2 cents
    ]
    res = mod.reconcile_balances(1000, postings, fee_bps=250)
    assert res["applied_tx_ids"] == ["tx-01", "tx-02", "tx-03"], f"Unexpected tx_ids: {res}"
    assert res["total_fees_cents"] == 10, f"Expected 10 cents total fees, got {res['total_fees_cents']}"
    assert res["closing_cents"] == 1090, f"Expected closing_cents=1090, got {res['closing_cents']}"


def test_empty_and_credit_only():
    mod = load_ledger()
    res = mod.reconcile_balances(250, [{"tx_id": "c1", "amount_cents": 150}], fee_bps=500)
    assert res == {
        "closing_cents": 400,
        "total_fees_cents": 0,
        "applied_tx_ids": ["c1"],
    }


if __name__ == "__main__":
    passed = 0
    total = 2
    errors = []
    for fn in (test_deduplication_and_rounding, test_empty_and_credit_only):
        try:
            fn()
            passed += 1
        except Exception as exc:
            errors.append(f"{fn.__name__}: {exc}")

    reward = 1.0 if passed == total else 0.0
    out_dir = Path("logs/verifier")
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "reward": reward,
        "passed_tests": passed,
        "total_tests": total,
        "pass_fraction": round(passed / total, 4),
        "errors": errors,
    }
    (out_dir / "reward.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (out_dir / "reward.txt").write_text(f"{reward}\\n", encoding="utf-8")
    sys.exit(0 if reward == 1.0 else 1)
'''

RUN_TESTS_SH = """#!/usr/bin/env bash
set -uo pipefail
python3 tests/test_outputs.py
exit $?
"""


def init_example_task(task_dir: Path, template_toml: Path) -> None:
    (task_dir / "workspace" / "src").mkdir(parents=True, exist_ok=True)
    (task_dir / "tests").mkdir(parents=True, exist_ok=True)

    (task_dir / "instruction.md").write_text(INSTRUCTION_MD, encoding="utf-8")
    if template_toml.exists():
        toml_text = template_toml.read_text(encoding="utf-8").replace("{{TASK_ID}}", task_dir.name)
    else:
        toml_text = f'[task]\nid = "{task_dir.name}"\n[verifier]\nenvironment_mode = "separate"\n'
    (task_dir / "task.toml").write_text(toml_text, encoding="utf-8")
    (task_dir / "Dockerfile").write_text(DOCKERFILE_TXT, encoding="utf-8")
    (task_dir / "workspace" / "src" / "ledger.py").write_text(BUGGY_LEDGER_PY, encoding="utf-8")

    sol_path = task_dir / "solution.sh"
    sol_path.write_text(SOLUTION_SH, encoding="utf-8")
    sol_path.chmod(0o755)

    (task_dir / "tests" / "test_outputs.py").write_text(TEST_OUTPUTS_PY, encoding="utf-8")
    run_sh = task_dir / "tests" / "run-tests.sh"
    run_sh.write_text(RUN_TESTS_SH, encoding="utf-8")
    run_sh.chmod(0o755)


def run_separate_verifier_trial(task_dir: Path, apply_oracle: bool) -> dict[str, Any]:
    """Simulate Harbor/Verifiers separate-verifier lifecycle:
    1. Provision solver sandbox with only `workspace/` files.
    2. Optionally run `solution.sh` inside solver sandbox.
    3. Copy artifact `src/` into a fresh grading sandbox where `tests/` is mounted fresh.
    4. Run `tests/run-tests.sh` and read `logs/verifier/reward.json`.
    """
    with tempfile.TemporaryDirectory(prefix="solver_box_") as solver_tmp, \
         tempfile.TemporaryDirectory(prefix="verifier_box_") as verifier_tmp:
        solver_path = Path(solver_tmp)
        verifier_path = Path(verifier_tmp)

        shutil.copytree(task_dir / "workspace", solver_path, dirs_exist_ok=True)

        if apply_oracle:
            sol_res = subprocess.run(
                ["bash", str(task_dir.resolve() / "solution.sh")],
                cwd=solver_path,
                capture_output=True,
                text=True,
                timeout=30,
            )
            if sol_res.returncode != 0:
                return {
                    "reward": 0.0,
                    "error": f"solution.sh failed: {sol_res.stderr}",
                }

        # Collect artifacts from solver box into fresh verifier box
        shutil.copytree(solver_path / "src", verifier_path / "src", dirs_exist_ok=True)
        shutil.copytree(task_dir / "tests", verifier_path / "tests", dirs_exist_ok=True)

        grade_res = subprocess.run(
            ["bash", "tests/run-tests.sh"],
            cwd=verifier_path,
            capture_output=True,
            text=True,
            timeout=30,
        )
        reward_json_path = verifier_path / "logs" / "verifier" / "reward.json"
        if reward_json_path.exists():
            payload = json.loads(reward_json_path.read_text(encoding="utf-8"))
        else:
            payload = {"reward": 0.0, "error": "reward.json not created"}
        payload["exit_code"] = grade_res.returncode
        return payload


def validate_task_dir(task_dir: Path) -> dict[str, Any]:
    required_files = [
        "instruction.md",
        "task.toml",
        "Dockerfile",
        "solution.sh",
        "tests/run-tests.sh",
        "tests/test_outputs.py",
    ]
    missing = [f for f in required_files if not (task_dir / f).exists()]
    toml_data = tomllib.loads((task_dir / "task.toml").read_text(encoding="utf-8")) if not missing else {}

    dockerfile_text = (task_dir / "Dockerfile").read_text(encoding="utf-8") if (task_dir / "Dockerfile").exists() else ""
    dockerfile_Clean = ("solution.sh" not in dockerfile_text.split("#")[0]) and (
        "COPY tests" not in dockerfile_text
    )
    workspace_clean = not (task_dir / "workspace" / "tests").exists() and not (
        task_dir / "workspace" / "solution.sh"
    ).exists()
    leakage_check_passed = bool(dockerfile_Clean and workspace_clean)

    separate_mode = toml_data.get("verifier", {}).get("environment_mode") == "separate"

    baseline_res = run_separate_verifier_trial(task_dir, apply_oracle=False)
    oracle_res = run_separate_verifier_trial(task_dir, apply_oracle=True)

    # Also copy the verified oracle reward.json into task_dir/logs/verifier/reward.json for inspection
    logs_dir = task_dir / "logs" / "verifier"
    logs_dir.mkdir(parents=True, exist_ok=True)
    (logs_dir / "reward.json").write_text(json.dumps(oracle_res, indent=2), encoding="utf-8")

    all_passed = (
        len(missing) == 0
        and leakage_check_passed
        and separate_mode
        and baseline_res.get("reward") == 0.0
        and oracle_res.get("reward") == 1.0
    )

    return {
        "task_id": task_dir.name,
        "structural_missing_files": missing,
        "separate_verifier_mode": separate_mode,
        "leakage_check_passed": leakage_check_passed,
        "null_baseline_result": baseline_res,
        "oracle_solution_result": oracle_res,
        "null_baseline_reward": baseline_res.get("reward"),
        "oracle_solution_reward": oracle_res.get("reward"),
        "all_checks_passed": bool(all_passed),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a Harbor / Terminal-Bench task package.")
    parser.add_argument(
        "--task-dir",
        default="rl-env-skills/examples/fix-ledger-rounding-bug",
        help="Path to the task package directory",
    )
    parser.add_argument(
        "--init-example",
        action="store_true",
        help="Initialize the example fix-ledger-rounding-bug task package before validating",
    )
    args = parser.parse_args()

    task_dir = Path(args.task_dir)
    template_toml = Path(__file__).resolve().parent.parent / "templates" / "task.toml.tmpl"
    if args.init_example or not task_dir.exists():
        task_dir.mkdir(parents=True, exist_ok=True)
        init_example_task(task_dir, template_toml)

    report = validate_task_dir(task_dir)
    report_path = task_dir / "package_validation_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
