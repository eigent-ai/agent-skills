---
name: ml-failure-audit
description: General workflow for auditing ML CI failures, experiment regressions, training run failures, golden metric failures, and telemetry-backed ML work-product claims from local repositories, logs, metrics, configs, and artifacts. Use when Codex needs to decide whether an ML failure is a model/convergence issue, correctness bug, data/config issue, infrastructure/runtime issue, evaluation/gating policy issue, or unsupported claim, and produce structured evidence-backed outputs.
---

# ML Failure Audit

## Purpose

Audit ML failures from supplied artifacts without assuming the headline explanation is true. Use this skill when the user provides a repo, logs, W&B/MLflow/TensorBoard exports, CI artifacts, config files, or reports and asks for a diagnosis, go/no-go decision, or structured output.

## Core Workflow

1. **Locate evidence**
   - Find the repo root, log files, metric exports, configs, test definitions, golden values, and any requested output schema.
   - Treat raw logs, raw telemetry, configs, and source code as higher-trust than reports, PR text, summaries, or generated JSONs.

2. **Classify the failure**
   - Separate model/convergence signals from correctness, data, config, runtime, infra, and metric-policy signals.
   - Do not label a failure as model/convergence regression when only a performance, timeout, logging, or tolerance gate failed and correctness/loss checks passed.

3. **Recompute key facts**
   - Extract the failing metric/test, passed checks, final run state, key training counters, and relevant metric values.
   - Recompute numeric claims directly from raw artifacts when possible.
   - Record formulas for derived values such as throughput, relative error, finish rate, loss deltas, or token counts.

4. **Trace code paths**
   - Identify how the repo selects metrics/tests and how comparisons are made.
   - Cite exact source files and, when useful, function names or line snippets.

5. **Make a decision**
   - State whether this is a true ML regression, system correctness bug, infra/runtime issue, data/config issue, metric-policy issue, or unsupported claim.
   - Recommend the minimal policy or engineering action that protects correctness without over-blocking valid runs.

6. **Write outputs**
   - Follow the task's requested schema exactly.
   - If no schema is given, write a concise report with: evidence, classification, calculations, recommendation, and validation checks.

## Guardrails

- Do not run expensive GPU training unless the user explicitly requests it.
- Do not clone remote repos when a local checkout is supplied.
- Do not trust prose summaries until verified against raw artifacts.
- Do not infer OOM, convergence, stability, or success from missing logs alone.
- If the task asks for a file output, create the file; do not only answer in chat.

## Helper Script

Use `scripts/collect_failure_evidence.py` for a quick first pass over a repo and logs:

```bash
python3 <skill_dir>/scripts/collect_failure_evidence.py \
  --repo <repo-root> \
  --logs <log1> <log2> \
  --out <output.json>
```

The script is intentionally generic. It extracts failure lines, pass lines, metric-looking lines, config/source candidates, and nearby context windows. Use it to accelerate evidence gathering, not as the final diagnosis.

## References

- Read `references/workflow.md` for the detailed audit checklist and failure taxonomy.
- Read `references/output_guidance.md` when the user asks for structured JSON or a file deliverable.

## Short Prompt Pattern

Use a short realistic task prompt like:

```text
Use $ml-failure-audit to audit this ML CI failure from the provided repo and logs. Decide whether it is a real training regression or a gate/policy issue, and produce the requested output files.
```
