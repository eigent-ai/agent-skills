---
name: sandboxed-task-packaging
description: Package reproducible terminal and coding tasks into Harbor / Terminal-Bench and Verifiers HarborTaskset directories with isolated verification tests, oracle solution validation, and anti-tampering boundaries. Use this skill when asked to "create a Terminal-Bench or Harbor task", "package a containerized CLI benchmark task", "verify an agent environment with pytest", or "prevent agents from reading or modifying test files".
---

# Sandboxed Task Packaging (`sandboxed-task-packaging`)

## 1. Prerequisites
- Python 3.10+ with `tomllib` (standard library in Python 3.11+) and `subprocess` / `tempfile` / `shutil`.
- Optional container/sandbox runner: Docker, Harbor CLI (`uv tool install harbor`), or Prime Intellect `verifiers.v1.tasksets.harbor.HarborTaskset`.
- Strict separation of the four post-training concepts:
  1. **Task Dataset**: The versioned collection of packaged task directories (`instruction.md`, `task.toml`, `Dockerfile`, `solution.sh`, `tests/`), defining problem instances and verification logic.
  2. **Recorded Trajectories**: Terminal command histories, file diffs, and `/logs/verifier/reward.json` outputs captured when an agent harness runs inside a sandboxed task container.
  3. **Supervised Training Examples (SFT)**: Formatted `(instruction + terminal observations -> shell actions)` pairs curated from verified passing trajectories.
  4. **RL Policy Optimisation**: Policy gradient updates (e.g., GRPO, PPO) over action tokens using the verifier reward signal—never confused with packaging a task or running an oracle `solution.sh`.

## 2. Required Inputs
- **`task_id`** (`str`, kebab-case): Unique task directory name (e.g., `fix-ledger-rounding-bug`).
- **`instruction_text`** (`str`): Self-contained, unambiguous user prompt specifying the exact file paths, CLI inputs/outputs, and acceptance invariants (without leaking hidden test values).
- **`workspace_files`** (`dict[str, str]`): Initial broken or unimplemented source files staged inside the agent's working directory (e.g., `/app/src/`).
- **`oracle_solution_script`** (`str`): Executable bash script (`solution.sh`) that deterministically repairs or solves the workspace from its initial state.
- **`pytest_suite`** (`str`): Outcome-based `pytest` verification script (`tests/test_outputs.py`) that grades end-state artifacts and behavior rather than matching agent command strings.
- **`verifier_mode`** (`"separate"` or `"shared"`): Whether grading executes in a fresh container untouched by the agent (`separate`, recommended) or in the solver container (`shared`).

## 3. Procedure (Numbered Steps)
1. **Create the Split Task Directory Structure**:
   - Organize the task package into **Agent-Visible Files** (`Dockerfile`, `instruction.md`, `workspace/`) and **Held-Out Verifier/Oracle Files** (`task.toml`, `solution.sh`, `tests/run-tests.sh`, `tests/test_outputs.py`) that are excluded from the image layers accessible during the agent rollout phase.
2. **Author `task.toml` with Resource, Network, and Separate-Verifier Policies**:
   - Populate `task.toml` from `templates/task.toml.tmpl`.
   - Set `[agent].network_mode = "no-network"` (or explicit `"allowlist"`) so the agent cannot fetch external solutions during rollout.
   - Set `[verifier].environment_mode = "separate"` and declare `artifacts = ["/app/src", "/logs/artifacts"]` so `verifiers` / `harbor` copies only the declared output artifacts into a clean grading container where `tests/` is mounted fresh.
3. **Write Outcome-Based Verification Tests (`tests/test_outputs.py`)**:
   - Base the test suite on `templates/test_outputs.py.tmpl`.
   - Assert observable end states (e.g., running the compiled binary or importing the repaired Python module against edge-case inputs, verifying file checksums or schema invariants) rather than grepping bash history.
4. **Emit Structured Verifier Rewards (`/logs/verifier/reward.json`)**:
   - Configure `tests/run-tests.sh` to execute `pytest`, capture pass/fail counts, and write `/logs/verifier/reward.json` containing `{"reward": <0.0_or_1.0>, "passed_tests": <int>, "total_tests": <int>}` plus fallback `/logs/verifier/reward.txt`.
5. **Prove Solvability and Non-Triviality with Dual Sandbox Runs**:
   - Run `scripts/validate_task_package.py` on the task directory:
     - **Null/Broken Baseline Run**: Execute `tests/run-tests.sh` against the unmodified `workspace/` in an isolated temporary sandbox and verify that `reward == 0.0` (proving the task is not already solved at reset).
     - **Oracle Solution Run**: Execute `solution.sh` in a fresh copy of `workspace/`, stage `tests/` fresh into a separate grading directory, run `tests/run-tests.sh`, and verify that `reward == 1.0` (proving the task is solvable and the tests are accurate).

## 4. Expected Outputs
- `<task_dir>/instruction.md`: Agent-facing problem specification.
- `<task_dir>/task.toml`: Harbor / Verifiers v1 configuration file specifying timeouts, `[agent].network_mode`, and `[verifier].environment_mode = "separate"`.
- `<task_dir>/Dockerfile`: Reproducible container build specification pinning base image and system packages.
- `<task_dir>/workspace/`: Initial task files given to the agent at episode reset.
- `<task_dir>/solution.sh`: Verified reference oracle script.
- `<task_dir>/tests/run-tests.sh` & `<task_dir>/tests/test_outputs.py`: Held-out verification suite writing `/logs/verifier/reward.json`.
- `<task_dir>/package_validation_report.json`: Output of `scripts/validate_task_package.py` recording structural checks, leakage audits, null-baseline failure (`reward == 0.0`), and oracle pass (`reward == 1.0`).

## 5. Decision Rules
- **Separate vs. Shared Verifier Container (`[verifier].environment_mode`)**:
  - *Default to `"separate"`*: Prevents an agent with root access in its container from overwriting `pytest`, monkey-patching test runners, or leaving background processes that spoof output files.
  - *Use `"shared"` only when*: Grading inspects live kernel/process state that cannot be serialized via `/logs/artifacts/`, and ensure `tests/` is mounted only after the agent process is terminated.
- **Outcome Grading vs. Command-Trace Grading**:
  - Always grade the final artifact or service response. Never penalize an agent for using `python3 -c`, `awk`, or `sed` instead of `nano` or `vim` to edit a file.
- **Handling Interactive CLI Hang Risk**:
  - Include non-interactive flags (`-y`, `--no-pager`, `DEBIAN_FRONTEND=noninteractive`) in environment defaults and configure per-command timeout guardrails in the harness so agents do not hang inside interactive editors like `nano` or `vim`.

## 6. Failure Recovery
- **Null Baseline Passes (`baseline_reward > 0.0`)**:
  - *Cause*: Initial `workspace/` already contains the fix or tests are vacuous (`assert True`).
  - *Recovery*: Inspect `package_validation_report.json`, tighten assertions in `tests/test_outputs.py`, and ensure the bug is present in `workspace/`.
- **Oracle Solution Fails (`oracle_reward < 1.0`)**:
  - *Cause*: Missing dependency, path mismatch between `solution.sh` and `tests/test_outputs.py`, or overly brittle formatting assertion.
  - *Recovery*: Inspect `oracle_stdout` / `oracle_stderr` in `package_validation_report.json` and align `solution.sh` with the exact contract stated in `instruction.md`.
- **Test Leakage into Agent Workspace**:
  - *Cause*: `Dockerfile` copies `tests/` or `solution.sh` into `/app`.
  - *Recovery*: Remove `COPY tests/` and `COPY solution.sh` from `Dockerfile`; stage `tests/` only inside the separate verifier phase.

## 7. Observable Success Checks
- `package_validation_report.json` reports `"all_checks_passed": true`.
- `leakage_check_passed: true` (neither `solution.sh` nor `tests/` is copied into the agent workspace before grading).
- `null_baseline_reward == 0.0` (unmodified initial workspace fails the verification suite).
- `oracle_solution_reward == 1.0` (applying `solution.sh` in a clean sandbox and grading in a separate verifier directory produces `{"reward": 1.0}` in `reward.json`).
