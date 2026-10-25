---
name: popnow-video
description: Create and manage AI video jobs through the paid PopNow API. Use when asked to generate a video from text or an image, check a PopNow job, or download its outputs. Discover the model schema, quote the exact request, and obtain spending confirmation before creating a job. Requires a user-supplied PopNow API key.
---

# PopNow video

Use PopNow's commercial API from an agent workflow. This skill and its bundled Python helper are MIT licensed; model access and the hosted service are separate, paid services. Installing the skill does not include generation credits or an API key.

The helper is an upstream source snapshot. Before submitting a paid job, check the current [API reference](https://popnow.ai/api-reference). It expects the quote fields `maxCredits` and `quoteId`, and uses the existing `--confirm-credits` flag. If the live API no longer returns that contract, stop and use the current official documentation; do not invent a conversion, bypass the confirmation guard, or treat a missing price as zero. Do not derive current prices from examples or the helper's human-readable summaries.

## Setup and model discovery

Use Python 3.8 or newer and the standard library; no dependency installation is required. Run commands from this skill's directory. The user must supply their own `POPNOW_API_KEY` through the environment using their normal secret-management process. Never ask them to paste a key into a prompt or commit it to a project.

Start with model information rather than a generation call:

```bash
python3 scripts/popnow.py models --modality video --schema --json
python3 scripts/popnow.py model '<selected-model-id>' --json
```

Choose a currently available model that fits the requested task. Read its required inputs, supported durations, resolutions, aspect ratios, and media fields. Use explicit values supported by that schema. See [model discovery and compatibility](references/models.md) when selecting or changing a model.

## Quote, confirm, create

1. Agree on the prompt, model, input media, duration, and resolution. Choose a lower-cost supported configuration when the user has not specified one, then obtain their approval of the actual quote.
2. Quote the exact request. A quote is not a completed generation or an authorization to spend:

   ```bash
   python3 scripts/popnow.py quote --model '<selected-model-id>' \
     --prompt 'A paper boat drifting across a quiet lake' \
     --duration '<supported-duration>' --resolution '<supported-resolution>' --json
   ```

3. Check the returned request and quote against the current API contract. Show the user the quoted maximum cost and its reported unit, together with the selected configuration. Do not promise a fixed exchange rate, refund, or free generation.
4. Only after explicit spending confirmation, create the same request. Replace every placeholder; `--confirm-credits` takes the integer `maxCredits` from the accepted quote, not a manually calculated monetary amount:

   ```bash
   python3 scripts/popnow.py create --model '<selected-model-id>' \
     --prompt 'A paper boat drifting across a quiet lake' \
     --duration '<supported-duration>' --resolution '<supported-resolution>' \
     --confirm-credits '<approved-maxCredits>' \
     --idempotency-key '<one-stable-key-for-this-job>' --json
   ```

The helper re-quotes before creation and refuses to start if the returned maximum is absent, not an integer, or above the approved cap. If the model, input, duration, resolution, or cost changes, obtain a fresh quote and confirmation. A successful submission means a job was accepted; it does not mean the video has finished.

## Input media

For image-to-video, use `--image` with an appropriate public URL or an existing `popnow://` URI. Use `--last-image` only when the chosen schema declares a closing-frame input. Keep the same media references between quote and create.

Local file paths passed to media flags are uploaded by the helper, including while building a quote request. Obtain the user's permission to upload a local file before using those flags. Prefer an existing approved media reference; do not upload private files merely to inspect pricing. Use `--set key=value` or `--input-file` only for fields documented in the chosen model schema.

## Monitor and collect results

Save the accepted `taskId` and the stable idempotency key with the logical job. If submission has an ambiguous network result, reconcile the existing job or repeat the identical request with that same key according to the current API contract. Do not generate a new key just because a response timed out.

```bash
python3 scripts/popnow.py status '<taskId>' --json
python3 scripts/popnow.py wait '<taskId>' --timeout 1200 --json
python3 scripts/popnow.py download '<taskId>' --out ./output --json
```

A local polling timeout does not cancel or fail the remote job. Resume monitoring its existing ID. Download only succeeded outputs, and never forward an API bearer key to an output URL. The bundled downloader sends a User-Agent header to media URLs without the API Authorization header. Treat signed media URLs as sensitive and temporary.

Report the actual final state and output paths. The `retry` command creates a new billed job; do not use it as a substitute for checking an accepted job. `purge` permanently removes task content. Both require a separate, explicit user decision and are outside the default generation workflow.

## Sources and license

Adapted from the PopNow team's public [popnow-video skill](https://github.com/popnow-ai/popnow-skills/tree/main/skills/popnow-video). See [source and compatibility notes](references/models.md) and the preserved [MIT license](LICENSE). Official [documentation](https://popnow.ai/docs) and [MCP connection guide](https://popnow.ai/docs/mcp) describe the hosted service. This catalog adaptation has not been validated by running paid model calls or an Eigent runtime session.
