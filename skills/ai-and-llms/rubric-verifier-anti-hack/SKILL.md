---
name: rubric-verifier-anti-hack
description: Engineer evidence-grounded verifiers and multi-objective reward functions that isolate rubric criteria, rank state snapshots per criterion, separate controllable process scores from uncontrollable environment failures, and detect reward hacking or "confident liar" false positives. Use this skill when asked to "build a verifier or reward function", "design an LLM judge rubric", "detect reward hacking or invalid successes", or "prevent cascading rubric errors".
---

# Rubric Verifier & Anti-Hack Engineering (`rubric-verifier-anti-hack`)

## 1. Prerequisites
- Python 3.10+ runtime with standard library (`json`, `math`, `re`, `pathlib`).
- Ground-truth environment state snapshots (`state_snapshots` or screenshots/DOM/file-system states) recorded alongside agent claims during trajectory execution.
- Strict distinction across the four post-training stages:
  1. **Task Dataset**: The user goal $g$, rubric criteria schema, and reference ground-truth invariants.
  2. **Recorded Trajectories**: The multi-step sequence of observations, actions, ground-truth state snapshots $s_0 \dots s_T$, and verifier scores $(s_{\text{proc}}, s_{\text{out}})$.
  3. **Supervised Training Examples (SFT)**: Trajectory subsets filtered by high verifier accuracy ($s_{\text{out}} = 1 \land s_{\text{proc}} \ge \tau \land \text{no reward hack}$).
  4. **RL Policy Optimisation**: Online parameter updates driven by composite rewards + group-relative advantages—never equated with running the offline verifier audit script itself.

## 2. Required Inputs
- **`task_goal`** (`str`): Exact user prompt / instruction $g$ given to the agent.
- **`rubric_spec`** (`dict`, conforming to `templates/rubric_schema.json`): List of atomic criteria $c_1 \dots c_K$, weights, conditional flags, and negative side-effect checks.
- **`trajectories`** (`list[dict]`): Recorded rollouts containing `agent_final_claim`, `action_history`, `state_snapshots` (each with step index, ground-truth state fields, and environment blocker flags), and `token_count`.

## 3. Procedure (Numbered Steps)
1. **Generate the Rubric Blind to Agent Behavior (`01 · Generate Rubric`)**:
   - Derive rubric criteria $c_1 \dots c_K$ strictly from `task_goal` $g$ before inspecting any agent trajectory or screenshot (`rubric_generator_saw_trajectory = False`).
   - Audit every criterion against `task_goal` to eliminate **phantom criteria** (unrequested requirements such as asking for total hotel price when only asked for the nearest coffee shop).
2. **Enforce Error Isolation Across Criteria (No Cascading Penalties)**:
   - Formulate downstream criteria relative to the entity selected by the agent in upstream steps (`evaluate_relative_to_upstream_selection: true`).
   - Example: If $c_1$ checks whether the agent picked the person with the longest surname and $c_2$ checks whether the agent reported the chosen person's net worth accurately, a mistake on $c_1$ penalizes **only** $c_1$ and never cascades to $c_2$.
3. **Compute the State-to-Criterion Relevance Matrix (`02 · Relevance Matrix`)**:
   - Rather than feeding all $T$ state snapshots into one context window or truncating to the final frame, score every snapshot $s_t$ against every criterion $c_k$ (`relevance(s_t, c_k)`).
   - Select the **top-$k$** most relevant state snapshots per criterion so no intermediate evidence (e.g., an error banner at step 4 or an unauthorized test-file edit at step 6) is lost.
4. **Run the Two-Stage Reality Check (`03 · Reality Check — State Overrides Claims`)**:
   - Stage A (Claim Check): Parse what `agent_final_claim` asserts it accomplished.
   - Stage B (Ground-Truth Verification): Evaluate each criterion strictly against its top-$k$ ground-truth `state_snapshots`.
   - Whenever Stage A asserts success while Stage B shows an unmet invariant, flag `"confident_liar_detected": true` and force `s_out = 0`.
5. **Separate Process Score ($s_{\text{proc}}$), Outcome Score ($s_{\text{out}}$), and Uncontrollable Failures**:
   - Classify any environment blocker (`login_wall`, `captcha`, `item_out_of_stock`, `entity_non_existent`, `sandbox_infra_unreachable`) as **uncontrollable**.
   - Exclude uncontrollable blockers from the controllable process denominator so an agent that executes valid steps up to an out-of-stock wall receives full controllable process credit ($s_{\text{proc}} = 1.0$) while its binary outcome remains $s_{\text{out}} = 0$.
   - Apply a post-hoc penalty for **unsolicited side effects** (e.g., modifying files outside scope or submitting unrequested orders).
6. **Scan for Reward-Hacking Signatures and Apply Group-Relative Conciseness Bonus**:
   - Check action traces for explicit reward-hacking patterns: modifying `tests/` or `conftest.py`, hardcoding expected test outputs via `sys.exit(0)` / monkey-patching, or exploiting deterministic simulator tie-breaks.
   - Across a rollout group sharing the same task prompt, award a **group-relative conciseness bonus** (`+0.10` scaled by relative token efficiency) **only** to rollouts that achieve $s_{\text{out}} = 1$ without reward-hacking flags, counteracting chain-of-thought length bloat without guessing an arbitrary fixed token cap $N$.
7. **Calibrate the Verifier Against Held-Out Human Labels**:
   - Run `scripts/audit_verifier_rubric.py` to score trajectories, detect false positives, and compute Cohen's $\kappa$ agreement and False Positive Rate (FPR) against a held-out ground-truth label split.

## 4. Expected Outputs
- `<output_dir>/verifier_audit_report.json`: Complete audit report containing:
  - Rubric hygiene checks (`phantom_criteria_removed`, `cascading_dependencies_isolated`).
  - Per-trajectory `relevance_matrix`, `s_proc` (float in `[0, 1]`), `s_out` (0 or 1), `failure_category` (`none`, `controllable_error`, `uncontrollable_env_blocker`, `confident_liar_hallucination`, `reward_hack_tampering`), and `group_shaped_reward`.
  - Calibration metrics against held-out labels: `naive_judge_fpr`, `universal_verifier_fpr`, and `cohens_kappa`.

## 5. Decision Rules
- **Deterministic Verifier vs. Rubric Verifier**:
  - *If exact functional equivalence is checkable via unit tests or symbolic math*: Use a deterministic verifier in a separate sandbox (`sandboxed-task-packaging`) as primary $s_{\text{out}}$.
  - *If tasks are open-ended, multi-step UI/web workflows, or require partial process credit*: Combine deterministic state checks with the 4-stage Universal Verifier rubric pipeline.
- **Handling Uncontrollable Failures in Downstream Data**:
  - Never penalize the policy with negative reward when `failure_category == "uncontrollable_env_blocker"` or when a grading sandbox is unreachable; either mask the rollout from the RL batch or score its controllable process prefix via $s_{\text{proc}}$.
- **Preventing Verifier Overfitting**:
  - Hold out at least two-thirds ($\ge 67\%$) of human-annotated trajectories as an untouched test split when iterating on verifier prompts or rubric rules.

## 6. Failure Recovery
- **High Verifier False Positive Rate ($\text{FPR} > 0.10$)**:
  - *Cause*: Verifier is trusting `agent_final_claim` or only checking the final frame instead of intermediate ground-truth state snapshots.
  - *Recovery*: Enable the two-stage Reality Check (`pixels/state override claims`) and verify that `top_k` relevance retrieval includes intermediate tool/state outputs.
- **Artificially Deflated Process Scores on Valid Trajectories**:
  - *Cause*: Phantom rubric criteria or cascading penalties from an early minor error.
  - *Recovery*: Strip any criterion whose keywords are absent from `task_goal` and set `evaluate_relative_to_upstream_selection: true` on dependent steps.
- **Chain-of-Thought Length Explosion During RL**:
  - *Cause*: Pure binary outcome reward with no efficiency pressure.
  - *Recovery*: Enable the group-relative conciseness bonus among passing rollouts (`s_out == 1`) rather than imposing a hard token truncation threshold that clips valid reasoning early in training.

## 7. Observable Success Checks
- `verifier_audit_report.json` exists and reports `"all_checks_passed": true`.
- `phantom_criteria_detected` catches and removes unrequested rubric items before scoring.
- Error-isolation check confirms that an upstream selection error penalizes only the upstream criterion while awarding full credit on accurate downstream execution.
- Confident-liar trajectories (where the agent claims success despite a failed state or tampered test) receive `s_out == 0` and `"confident_liar_detected": true`.
- Calibration check achieves `universal_verifier_fpr == 0.0` and `cohens_kappa >= 0.80` on the benchmark test cases.
