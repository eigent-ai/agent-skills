---
name: multi-turn-env-scaffold
description: Design and scaffold reproducible multi-turn reinforcement-learning agent environments with explicit task datasets, state reset behaviour, deterministic per-turn seeding, and stratified difficulty sampling. Use this skill when asked to "build an RL environment for an agent", "scaffold a Verifiers taskset or multi-turn gym", "define observations, actions, and termination rules", or "reduce rollout variance across GRPO groups".
---

# Multi-Turn Environment Scaffold (`multi-turn-env-scaffold`)

## 1. Prerequisites
- Python 3.10+ runtime with standard library (`json`, `hashlib`, `random`, `dataclasses`, `pathlib`).
- Optional for Prime Intellect integration: `verifiers` (`verifiers.v1` modular `Task` / `Taskset` / `Env` API or legacy `verifiers` `MultiTurnEnv`).
- Clear separation of the four post-training artifacts before writing any code:
  1. **Task Dataset**: Immutable rows specifying initial prompts, seeds, difficulty parameters, and ground-truth verification targets (`TaskData`).
  2. **Recorded Trajectories**: Multi-turn interaction histories (state, observation, action, step/terminal rewards) produced when an agent harness executes against an environment instance.
  3. **Supervised Training Examples (SFT)**: Filtered, formatted `(messages -> target_completion)` pairs exported from high-scoring trajectories for cross-entropy imitation learning.
  4. **RL Policy Optimisation**: Online or asynchronous weight updates (e.g., GRPO, CISPO, PPO) computed from token-level log-probabilities and group-relative advantages—never conflated with merely exporting trajectories or task rows.

## 2. Required Inputs
- **`env_name`** (`str`, kebab-case): Package/environment identifier (e.g., `pytest-repair-env` or `grid-nav-env`).
- **`state_schema`** (`dict`): Mutable per-episode state keys initialized on reset (e.g., `board`, `grid_pos`, `files_snapshot`, `turn_count`, `terminated`, `winner`).
- **`action_contract`** (`dict`): Expected format of the agent's action (e.g., XML tag `<action>...</action>` or structured tool call) and valid action domain.
- **`termination_conditions`** (`list[str]`): Explicit stopping criteria (`goal_reached`, `max_turns_reached`, `unrecoverable_syntax_abort`).
- **`difficulty_range`** (`tuple[float, float]`): Minimum and maximum difficulty or stochasticity parameter (e.g., `min_noise_prob`, `max_noise_prob`) for stratified batch construction.
- **`num_tasks`** (`int`): Number of deterministic task instances to generate in the initial task dataset.

## 3. Procedure (Numbered Steps)
1. **Decompose Environment into Taskset, Harness, and Runtime**:
   - Follow the `verifiers.v1` modular pattern (`taskset × harness × runtime`): keep task definitions and scoring rules inside the **Taskset** (`TaskData` + `Task` hooks), keep agent prompting/tool-loop mechanics inside the **Harness**, and isolate execution inside the **Runtime** (`subprocess` for local debugging, `docker` or remote sandboxes for isolation).
2. **Define Immutable Task Dataset (`TaskData`) with Stratified Difficulty**:
   - Create a dataset where each row has a stable `task_id`, `example_seed`, `difficulty_bucket`, `initial_prompt`, and `ground_truth`.
   - Partition `num_tasks` evenly across difficulty strata spanning `difficulty_range` so mini-batches never cluster exclusively on trivial or impossible instances.
3. **Implement Isolated Episode Reset (`reset` / `setup_state`)**:
   - On every episode start, construct a fresh copy of `state_schema` from the immutable `TaskData` row without mutating shared class attributes or global filesystem paths.
   - Derive initial environment configuration (such as starting player, obstacle placement, or initial file state) strictly from `example_seed`.
4. **Enforce State-Conditioned Deterministic Turn Seeding**:
   - Whenever the environment or an opponent/simulator takes a stochastic step at turn $t$, compute a deterministic turn seed:
     $$\text{turn\_seed} = \text{SHA256}(\text{example\_seed} \mathbin{\Vert} \text{canonical\_state\_json} \mathbin{\Vert} t)$$
   - Seed a local `random.Random(turn_seed)` instance. This guarantees that two rollouts in the same GRPO group that reach an identical intermediate state receive identical environment transitions, isolating policy variance from environment noise.
5. **Implement Step Transition and Soft Invalid-Action Handling (`step` / `env_response`)**:
   - Parse the agent's action according to `action_contract` ( referencing `templates/verifiers_v1_taskset_template.py`).
   - Do **not** terminate the episode on the first malformed or invalid move when training small or mid-sized models; instead, record an invalid-action counter in `state`, apply a bounded per-step penalty (e.g., `-0.1`), return an observation explaining why the action was invalid, and continue until `max_turns` (e.g., 8 turns).
6. **Eliminate Tie-Break Biases in Environment Simulators**:
   - If the environment includes an algorithmic opponent or simulator (such as minimax or heuristic pathing) where multiple responses share the same optimal value, break ties using the state-conditioned `local_rng.choice(best_moves)` rather than selecting index `0`. This prevents the policy from memorizing a deterministic opponent trajectory.
7. **Generate and Self-Test the Scaffold**:
   - Run `scripts/scaffold_env.py` to generate the environment module, task dataset JSONL, and Verifiers v1 wrapper, and execute the built-in determinism and reset-isolation verification suite.

## 4. Expected Outputs
- `<output_dir>/<env_name>/env_core.py`: Standalone, dependency-free Python environment implementing `reset()`, `step()`, state-conditioned seeding, and soft invalid-action penalties.
- `<output_dir>/<env_name>/verifiers_v1_taskset.py`: `verifiers.v1`-compatible `TaskData`, `TaskConfig`, `Task` (`@vf.reward`, `@vf.stop`, `@vf.metric`), and `Taskset` module generated from `templates/verifiers_v1_taskset_template.py`.
- `<output_dir>/<env_name>/tasks_dataset.jsonl`: Stratified **task dataset** (explicitly labeled `"artifact_type": "task_dataset"`).
- `<output_dir>/<env_name>/scaffold_check_report.json`: Automated verification report confirming reset isolation, state-hash turn determinism, and stratified bucket balance.

## 5. Decision Rules
- **Single-Turn vs. Multi-Turn**: Use a single-turn task when the observation is static and requires one completion; use a stateful multi-turn environment whenever actions mutate world state, invoke tools, or require iterative error recovery.
- **Hard Termination vs. Soft Penalty on Invalid Actions**:
  - *If base model format compliance is < 80%*: Use soft continuation with a `-0.1` step penalty and explicit error feedback up to `max_turns` so rollouts still reach terminal states and provide non-zero reward variance.
  - *If evaluating a frontier model under strict benchmark rules*: Optionally cap consecutive invalid actions at 2 before aborting.
- **Subprocess vs. Container Runtime**:
  - *If actions only mutate in-memory Python state*: `subprocess` or in-process execution is sufficient.
  - *If actions execute shell commands or modify disk files*: Require a per-rollout isolated directory or Docker container (`sandboxed-task-packaging`).

## 6. Failure Recovery
- **Zero Reward Variance Across Rollout Group (All 0.0)**:
  - *Cause*: Environment difficulty is too high (e.g., pure optimal opponent from step 0) or hard termination kills every rollout on turn 1.
  - *Recovery*: Widen `difficulty_range` to include easier strata (e.g., `noise_prob` in `[0.2, 0.8]`) and switch invalid moves from immediate loss to `-0.1` soft penalty.
- **Reward Fluctuation Across Mini-Batches**:
  - *Cause*: Random sampling drew a batch of all-hard or all-easy tasks.
  - *Recovery*: Enable stratified batch sampling (`difficulty_bucket` round-robin ordering in `tasks_dataset.jsonl`).
- **State Leakage Between Rollouts**:
  - *Cause*: Mutable default arguments or shared class dictionaries mutated during `step()`.
  - *Recovery*: Enforce `copy.deepcopy()` on initial state inside `reset()` and verify that `scaffold_check_report.json` reports `reset_isolation_passed: true`.

## 7. Observable Success Checks
- `scaffold_check_report.json` exists and reports `"all_checks_passed": true`.
- Re-running two rollouts with the same `example_seed` and identical action sequences produces byte-identical state hashes and rewards (`determinism_check_passed: true`).
- Mutating state in rollout 1 and calling `reset()` for rollout 2 leaves rollout 2's initial state identical to a fresh instance (`reset_isolation_passed: true`).
- `tasks_dataset.jsonl` contains equal counts across all configured difficulty strata (`stratification_balance_passed: true`).
