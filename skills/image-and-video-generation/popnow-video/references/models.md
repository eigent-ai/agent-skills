# Model discovery and compatibility

Do not use a static price table to authorize a generation. Model availability, inputs, supported media, and costs can change.

## Inspect the live schema

1. List video models with `python3 scripts/popnow.py models --modality video --schema --json`.
2. Inspect the selected model with `python3 scripts/popnow.py model '<model-id>' --json`.
3. Read `available`, `inputSchema.required`, properties, enumerations, and numeric limits. Pick the actual text-to-video or image-to-video task, rather than inferring capability from a model family name.
4. Pass only supported fields. `--duration` maps to `duration_seconds`; `--resolution` maps to `resolution`; `--aspect-ratio` maps to `aspect_ratio`. Image flags are mapped to the model's declared singular or plural media field.
5. Quote the exact complete input and report the returned cost and unit. Re-quote after changes.

The bundled helper expects `/api/v1/models`, `/api/v1/jobs/quote`, `/api/v1/jobs/createTask`, and `/api/v1/jobs/recordInfo`. Its confirmation guard requires the quote's integer `maxCredits` and `quoteId`; its flag is literally `--confirm-credits`. These names describe this source snapshot's protocol, not a promise about billing units or exchange rates. If the current API reference or live response differs, stop before creation and follow the current official contract. Do not rename fields speculatively or bypass a failed guard.

## Provenance

- Upstream: [popnow-ai/popnow-skills](https://github.com/popnow-ai/popnow-skills).
- Source revision: [`7116ca7a328943acfe799a0f87084abbc69992c6`](https://github.com/popnow-ai/popnow-skills/tree/7116ca7a328943acfe799a0f87084abbc69992c6/skills/popnow-video).
- `scripts/popnow.py` is copied byte-for-byte from that revision; its protocol fields and implementation are unchanged.
- `SKILL.md` and this reference are adapted for this catalog's concise frontmatter and workflow format. This reference replaces the upstream dated model/price snapshot with discovery instructions.
- The original MIT copyright notice and license are retained in `../LICENSE`. The hosted backend and model service are commercial services outside that source license.
- Validation for this catalog contribution is static only. No API credentials were supplied, no uploads or model calls were performed, and no runtime compatibility or output-quality claim is made.

Current sources: [API reference](https://popnow.ai/api-reference), [documentation](https://popnow.ai/docs), [pricing](https://popnow.ai/pricing).
