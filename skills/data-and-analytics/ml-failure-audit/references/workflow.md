# ML failure audit workflow

## Evidence hierarchy

Prefer evidence in this order:

1. Raw logs, raw telemetry, raw metric exports, and source code.
2. Config files, command lines, environment captures, metadata, manifests.
3. Generated analysis artifacts, dashboards, reports, PR text, notes.
4. Human claims without backing artifacts.

When artifacts conflict, trust the rawer source and explicitly flag the conflict.

## Failure taxonomy

Use these categories as a starting point:

- `model_convergence_regression`: loss/quality metrics degrade under comparable conditions, with valid training/eval evidence.
- `training_correctness_bug`: loss denominator, masking, distributed reduction, checkpoint restore, data ordering, or numerical behavior is wrong.
- `data_or_config_issue`: dataset, batch size, sequence length, seed, hyperparameter, model shape, or config axis changed unexpectedly.
- `infra_or_runtime_issue`: OOM, host failure, package/runtime drift, missing files, worker crash, timeout, network/storage issue.
- `metric_policy_issue`: gate fails because the metric selection, tolerance, directionality, aggregation, or golden baseline policy is wrong.
- `observability_issue`: logs/metrics are missing, truncated, sampled incorrectly, or not comparable.
- `unsupported_claim`: report/PR/recommendation overstates what the raw artifacts prove.

Multiple categories may apply; identify the primary blocker.

## Minimum audit checklist

1. What failed exactly?
   - Test name, metric name, assertion, exit code, failing step, or failed job.

2. What passed at the same time?
   - Passing loss checks, deterministic checks, memory checks, validation metrics, final checkpoint, or completed iterations.

3. Was the run complete and comparable?
   - Final iteration, consumed samples/tokens, train/eval state, missing artifacts, changed axes.

4. How does the code decide pass/fail?
   - Metric selection, thresholds, tolerances, deterministic vs approximate comparison, aggregation window, directionality.

5. What calculation decides the diagnosis?
   - Relative error, throughput, finish rate, loss delta, token-normalized denominator, coverage percentage, etc.

6. What should change?
   - Fix model/training code, rerun controlled experiment, repair data/config, change infra, revise metric gate, or mark claim unsupported.

## Recommendation language

Be explicit:

- "This is a model/convergence regression because..."
- "This is not a convergence regression; it is a metric-policy issue because..."
- "Hold the change because evidence is confounded by..."
- "Ship only after..."
- "Make the performance metric non-blocking / one-sided / informational..."

Avoid vague labels like "maybe unstable" unless the evidence is genuinely incomplete.
