# Agent Skills

A collection of skills for AI coding agents when building Eigent. 

Skills follow the [Agent Skills](https://agentskills.io/) format.

## Available Skills

1. **ui-ux-design** (`skills/eigent-design/SKILL.md`)
   - **Use when:** You need to plan a new UI (design guide) or audit an existing UI (design review).
   - **Category covered:** UI/UX design, token compliance, interaction quality, accessibility.
   - **Feature:** Two modes: `Design Guide` (pre-build spec) and `Design Review` (post-build checklist with severity).
   - **How it works:** Reads design references and outputs a structured markdown guide/review with concrete tokens, states, and fixes.
   - **Result:** Implementation-ready design specs or actionable UI review findings.

2. **eigent-blog** (`skills/eigent-blog-update/SKILL.md`)
   - **Use when:** You need to create, edit, or structure blog posts for Eigent.
   - **Category covered:** Blog content operations, frontmatter metadata, blog asset organization.
   - **Feature:** Includes `generate_post.py` template generation and frontmatter/directory rules.
   - **How it works:** Generates or validates post structure (`.md/.mdx`), required metadata, and correct asset paths.
   - **Result:** Publish-ready blog posts with consistent formatting and SEO-friendly metadata.

3. **eigent-usecases** (`skills/eigent-usecase-update/SKILL.md`)
   - **Use when:** You need to create, edit, or manage usecase entries for Eigent.
   - **Category covered:** Usecase JSON authoring, media asset linkage, SEO metadata.
   - **Feature:** Includes `generate_usecase.py` plus JSON/template and naming conventions.
   - **How it works:** Builds valid usecase JSON with required fields and maps image/video assets in `public/gallery/`.
   - **Result:** Valid, display-ready usecase entries with consistent structure and discoverability.
