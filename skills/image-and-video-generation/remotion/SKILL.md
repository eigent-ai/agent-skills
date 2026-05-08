---
name: remotion
description: Create videos programmatically using React (Remotion) or generate mathematical/conceptual animations (Manim). Use when the user asks to make a video, animation, product demo, tutorial, social clip, or branded video pipeline. Triggers: /remotion-video, /video-animation, /video-toolkit
---

## Overview

Make videos programmatically — describe what you want and the skill writes the components, handles timing, animations, and renders to MP4. No video editor needed. Covers three workflows: React-based video composition, mathematical animation, and a full branded production pipeline.

---

## /remotion-video

Core skill. Takes a concept or script and produces a full Remotion React project — scenes, transitions, timing, and animations. Renders to MP4. Works for tutorials, product demos, social content, and data stories.

### Workflow

1. Clarify the video concept, duration, target format (landscape/portrait/square), and any brand colors or assets.
2. Scaffold a Remotion project with `@remotion/cli` if one doesn't exist.
3. Write React components for each scene — use `useCurrentFrame`, `interpolate`, and `spring` for timing and animation.
4. Wire scenes into a `Composition` with correct `durationInFrames` and `fps`.
5. Render to MP4 via `npx remotion render`.

### Example prompts

| Use case | Task prompt |
|---|---|
| Product demo | Create a 30-second product demo video for a password manager app. Show the browser extension detecting a login form, autofilling credentials, and a vault unlock animation. |
| Tutorial | Make a 60-second animated tutorial explaining how JWT authentication works. Use simple shapes and text animations, no talking head. |
| Social clip | Create a 15-second announcement video for our new feature launch. Bold text reveals, dark background, ends with the product logo and a CTA. |

---

## /video-animation

Produces 3Blue1Brown-style mathematical and conceptual animations using Manim. Describe the concept and the skill plans scenes, writes the animation code, and iterates until the visual matches the explanation.

### Workflow

1. Understand the concept to animate — ask for the target audience and desired runtime if unclear.
2. Break the explanation into discrete visual scenes (one idea per scene).
3. Write Manim Python code for each scene using `ManimCE` conventions.
4. Run scenes and review output; iterate on timing, labels, and transitions.
5. Concatenate scenes into a final render.

### Example prompts

| Use case | Task prompt |
|---|---|
| CS concept | Animate how a binary search tree insertion works. Show each step visually — node comparisons, pointer updates, and the final tree shape. |
| Math explainer | Create an animation explaining compound interest over 30 years. Show the curve vs linear growth, with annotations at key milestones. |
| System design | Animate how a message queue works: producer pushing messages, consumer pulling them, and what happens when the consumer is slow. |

---

## /video-toolkit

Full branded production pipeline — combines Remotion with ElevenLabs voiceover, custom transitions, a theme/brand profile system, and FFmpeg post-processing. Tracks project state across sessions so you can iterate without starting over.

### Workflow

1. Collect brand profile: colors (hex), fonts, logo asset, voiceover tone/style.
2. Generate ElevenLabs voiceover from script; save audio with timestamps for sync.
3. Build Remotion composition with branded transitions and the voiceover timeline.
4. Post-process with FFmpeg: normalize audio, add subtitles if requested, export final MP4.
5. Save project state to a JSON manifest so future sessions can resume or produce variants.

### Example prompts

| Use case | Task prompt |
|---|---|
| Brand video | Build a 90-second brand explainer video. Use our brand colors [hex codes], generate a voiceover from this script, and add smooth slide transitions between each section. |
| Course content | Create a series of 5 short explainer videos (2 min each) from these lesson scripts. Consistent branding across all, with auto-generated subtitles. |
| Ad creative | Produce 3 variations of a 20-second ad for A/B testing — same script, different visual styles: minimal, bold, and animated. Export all three as MP4. |

---

## Dependencies

```bash
npm install @remotion/cli @remotion/player react react-dom
pip install manim
# ElevenLabs SDK (for /video-toolkit)
pip install elevenlabs
# FFmpeg must be installed on PATH
```
