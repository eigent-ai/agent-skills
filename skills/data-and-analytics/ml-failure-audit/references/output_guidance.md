# Output guidance

## If the task provides a schema

- Follow it exactly.
- Preserve required top-level keys.
- Use valid JSON, not Markdown-wrapped JSON.
- Put numeric values in numeric fields, not strings.
- Include source references that match the mounted artifact paths where possible.
- Validate with `python3 -m json.tool`.

## If the task asks for a report

Use a compact structure:

1. Diagnosis
2. Evidence table or bullet list
3. Calculations
4. Source-code/test logic
5. Recommendation
6. Validation checks / residual risk

## If no output location is specified

Write into the repo root unless the user says otherwise:

- `answer.json` for structured tasks.
- `answer.md` for concise prose.
- `audit_report.md` for broader reports.

## Good source references

Use paths plus enough context to be useful:

- `ci_log_1.log`: failing pytest block and final iteration lines.
- `tests/.../common.py`: comparison function, threshold logic, aggregation.
- `tests/.../model_config.yaml`: selected metrics and workload config.
- `raw_telemetry/runs.jsonl`: run state, finish rate, run IDs.
- `raw_telemetry/history/<run>.parquet`: step metrics and final anchors.

## Validation

Include checks that can be repeated without rerunning expensive training:

- JSON parses.
- Required fields are present.
- Formula matches numbers.
- Source files contain the cited metric/test logic.
- Logs contain the cited failure/pass lines.
