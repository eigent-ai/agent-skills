---
name: trajectory-rollout-curation
description: Collect, score, and audit multi-turn agent trajectories across rollout groups, preserve dual message-and-token trace masks, compute group-relative advantages, and filter verified trajectories into SFT datasets without conflating trajectory export with RL policy optimisation. Use this skill when asked to "collect and score agent trajectories", "prepare SFT warm-up data from rollouts", "compute GRPO group advantages", or "audit tokenization alignment on multi-turn traces".
---

# Trajectory Rollout Collection & Data Curation (`trajectory-rollout-curation`)

## 1. Prerequisites
- Python 3.10+ runtime with a target multi-turn environment (`env_core.py` from `multi-turn-env-scaffold` or a sandboxed task from `sandboxed-task-packaging`).
- A policy driver: scripted oracle policy, rule-based heuristic policy, random policy, or an OpenAI/Anthropic-compatible endpoint routed through an Interception Server.
- Strict four-way conceptual and file-level separation:
  1. **Task Dataset (`tasks_dataset.jsonl`)**: Input problem specifications (`task_id`, `example_seed`, `initial_prompt`, `ground_truth`). Contains **no** agent completions.
  2. **Recorded Trajectories (`recorded_trajectories.jsonl`)**: Full multi-turn episodes (`messages`, `state_trace`, `step_rewards`, `terminal_reward`, `group_advantage`, `token_segments` with `is_action_token` mask). Recording trajectories is **data collection / evaluation**, not model training.
  3. **Supervised Training Examples (`sft_examples.jsonl`)**: Filtered, successful trajectories (`s_out == 1`, zero invalid actions, no reward hacks) converted into `(messages, target_assistant_turns)` records for offline cross-entropy SFT warm-up.
  4. **RL Policy Optimisation**: Online or asynchronous gradient updates (e.g., GRPO, CISPO, PPO) where a live trainer consumes rollout batches, computes importance-sampled policy ratios from actor log-probabilities, and updates model weights. Exporting `recorded_trajectories.jsonl` or `sft_examples.jsonl` is **never** RL policy optimisation.

## 2. Required Inputs
- **`tasks_dataset_path`** (`Path`): Path to the input `tasks_dataset.jsonl`.
- **`env_module_path`** (`Path`): Path to the executable environment module (`env_core.py`).
- **`group_size`** (`int`, $\ge 2$): Number of rollouts sampled per task row to form a rollout group $G$.
- **`policy_mix`** (`list[str]`): Policies to execute across each group (e.g., `["scripted_optimal", "rule_based_heuristic", "noisy_heuristic", "random_policy"]` for local testing without paid LLM APIs).
- **`sft_filter_rules`** (`dict`): Minimum `s_out`, minimum `s_proc`, and maximum allowed `invalid_moves` for promoting a recorded trajectory into `sft_examples.jsonl`.

## 3. Procedure (Numbered Steps)
1. **Execute Grouped Rollouts per Task Row**:
   - Load each immutable `TaskData` row from `tasks_dataset.jsonl` and run `group_size` rollouts starting from `env.reset(task_row)`.
   - Because the environment uses state-conditioned turn seeding (`derive_turn_seed`), any two rollouts in the group that take identical actions experience identical environment transitions.
2. **Record Dual Message-and-Token Trace Graphs (`token_segments`)**:
   - At each turn, store both the logical message (`role`, `content`) and its pre-tokenized segment with an explicit `loss_mask` (`1` for agent action/reasoning tokens, `0` for system prompts, user prompts, and environment/tool observations).
   - Never flatten a multi-turn trajectory to raw text and re-tokenize it post-hoc during RL training, as many-to-one BPE boundary shifts (such as stripped trailing newlines in chat templates) corrupt token alignment between inference log-probs and trainer loss.
3. **Score Each Rollout and Compute Group-Relative Advantages**:
   - For rollout $i \in \{1 \dots G\}$ in group $g$, compute composite reward:
     $$R_{g,i} = w_{\text{out}}\, s_{\text{out},i} + w_{\text{proc}}\, s_{\text{proc},i} + b_{\text{concise},i} + \sum_t r_{\text{step},i,t}$$
   - Compute group mean $\mu_g = \frac{1}{G}\sum_{i=1}^G R_{g,i}$ and group standard deviation $\sigma_g$, then record the group-relative advantage:
     $$A_{g,i} = \frac{R_{g,i} - \mu_g}{\max(\sigma_g, \epsilon)}$$
   - Flag groups with $\sigma_g == 0.0$ as `"zero_variance_group": true` (which contribute zero gradient signal in GRPO).
4. **Review Trajectories for Failure Modes Before Exporting Data**:
   - Inspect rollout diagnostics for recurrent failure patterns: format non-compliance, invalid move penalties, fork/trap states, interactive shell hangs, or reward-hacking flags.
5. **Curate Supervised Fine-Tuning (SFT) Warm-Up Examples (`sft_examples.jsonl`)**:
   - Filter `recorded_trajectories.jsonl` using `sft_filter_rules`: retain only trajectories where `s_out == 1`, `invalid_moves == 0`, and `reward_hack_flags == []` (and optionally deduplicate or take the highest-reward trajectory per group).
   - Removing losing or malformed trajectories prevents baking suboptimal strategies or syntax errors into the SFT warm-up checkpoint.
6. **Emit the Data-Stage Distinction Audit (`curation_summary.json`)**:
   - Run `scripts/collect_and_curate_rollouts.py` to generate `recorded_trajectories.jsonl`, `sft_examples.jsonl`, and `curation_summary.json` with explicit counts and artifact-stage metadata.

## 4. Expected Outputs
- `<output_dir>/recorded_trajectories.jsonl`: Multi-turn rollout records conforming to `templates/trajectory_record_schema.json` (`"artifact_type": "recorded_trajectory"`).
- `<output_dir>/sft_examples.jsonl`: Filtered, high-reward conversational examples (`"artifact_type": "supervised_training_example"`).
- `<output_dir>/curation_summary.json`: Diagnostic report containing group reward statistics, zero-variance group counts, failure-mode breakdown, token-mask alignment checks, and an explicit `"rl_policy_optimisation_performed": false` declaration.

## 5. Decision Rules
- **When to Run SFT Warm-Up Before RL**:
  - *If the base model fails output formatting or makes frequent invalid moves ($> 20\%$ invalid actions)*: Curate 100–300 filtered trajectories from a teacher or scripted/heuristic policy into `sft_examples.jsonl` for a brief SFT warm-up before starting GRPO/RL.
  - *If the base model already follows format reliably and achieves non-zero pass@k*: Proceed directly to online RL rollouts to avoid narrowing exploration diversity.
- **Handling Zero-Variance Rollout Groups ($\sigma_g == 0$)**:
  - If all $G$ rollouts fail ($R_{g,i} = 0$) or all succeed identically, advantage $A_{g,i} = 0$; filter or down-weight zero-variance groups and adjust task difficulty parameters.
- **Synchronous vs. Asynchronous Rollout Collection**:
  - For long-horizon multi-turn agents where rollout duration has a heavy tail, decouple rollout workers from trainer GPUs via an async orchestrator (and bound off-policy staleness to $\le 3$ weight steps).

## 6. Failure Recovery
- **All Trajectories Rejected by SFT Filter (`sft_examples_count == 0`)**:
  - *Cause*: Policy mix is too weak for the task difficulty or `invalid_moves == 0` filter is too strict.
  - *Recovery*: Include a `scripted_optimal` or stronger teacher policy on the easiest difficulty stratum (`difficulty_bucket == "easy"`), or allow trajectories that recover from a single invalid move (`invalid_moves <= 1`) provided `s_out == 1`.
- **Token-to-Message Mismatch Detected**:
  - *Cause*: Post-hoc string concatenation and re-tokenization altered token boundaries.
  - *Recovery*: Preserve the exact token IDs / segments emitted at each turn via the `token_segments` array and compute action masks directly on those segments.

## 7. Observable Success Checks
- `recorded_trajectories.jsonl` contains `num_tasks * group_size` valid trajectory records with `"artifact_type": "recorded_trajectory"`.
- Every trajectory record includes `token_segments` where assistant turns have `loss_mask: 1` and system/user/environment turns have `loss_mask: 0` (`token_mask_alignment_passed: true`).
- `sft_examples.jsonl` contains only verified winning trajectories (`s_out == 1` and `invalid_moves == 0`) with `"artifact_type": "supervised_training_example"`.
- `curation_summary.json` reports `"all_checks_passed": true` and explicitly separates `task_dataset_count`, `recorded_trajectories_count`, `sft_examples_count`, and `rl_policy_optimisation_performed: false`.
