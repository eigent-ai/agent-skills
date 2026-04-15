---
name: instagram-reel-editor
description: Edits raw travel footage into polished Instagram Reels (9:16, 1080×1920) with cinematic color grading, beat-synced cuts, text overlays, transitions, and background music. Use when the user mentions editing a reel, travel reel, Instagram video, cutting footage, travel clips, reel from footage, or provides folders with destination subfolders and optional shared _music or _fonts.
---

# Instagram Reel Editor

Transforms raw travel footage folders into cinematic Instagram Reels (9:16 vertical, 1080×1920px).
Each destination folder becomes a standalone reel with music, text overlays, and cinematic effects.

**Requirements:** ffmpeg, Python 3, and `moviepy>=2.0`. The agent should be able to run shell commands, write files, and present output files to the user.

---

## Folder Contract

The user provides a root folder following this structure:

```
travel-project/
├── bali/                  ← destination folder (one reel per folder)
│   ├── clip1.mp4
│   ├── clip2.MOV
│   └── ...
├── tokyo/
│   └── ...
├── _music/                ← shared background music (randomly selected per reel)
│   ├── track1.mp3
│   └── track2.wav
└── _fonts/                ← shared fonts for text overlays
    └── Montserrat-Bold.ttf
```

**Rules:**
- Destination folders = any folder NOT starting with `_`
- `_music/` = shared pool; one track randomly selected per destination
- `_fonts/` = font(s) for text overlays; use first `.ttf` or `.otf` found
- Supported clip formats: `.mp4`, `.mov`, `.MOV`, `.MP4`, `.avi`, `.mkv`

---

## Reel Spec (Instagram Standard)

| Property | Value |
|---|---|
| Resolution | 1080 × 1920 px (9:16 vertical) |
| FPS | 30 fps |
| Duration | 15–60 seconds (target: 30s) |
| Audio | Stereo, 44.1kHz, normalized to -14 LUFS |
| Format | H.264 MP4, AAC audio |
| Text safe zone | 250px top and bottom margins |

---

## Cinematic Style Reference (Instagram Travel Reels 2024–2025)

Based on current trends from top travel creators (@muradosmann, @expertvagabond, @thewanderinglens):

**Pacing:**
- Hook clip: 1.5–2.5s (most dramatic or beautiful moment)
- Middle clips: 2–4s each
- Outro clip: 3–5s with fade to black
- Total clips: 8–15 clips for a 30s reel

**Transitions (in order of current popularity):**
1. `xfade=fade` – clean dissolve (universal)
2. `xfade=wipeleft` / `wiperight` – directional wipe
3. `xfade=slideleft` / `slideright` – motion slide
4. `xfade=circlecrop` – cinematic circle reveal
5. Cut on beat (no transition filter) – high energy sections

**Color Grading Presets (choose by destination mood):**
- `warm_golden` – Bali, Morocco, Mexico (warm shadows, lifted highlights)
- `cool_teal` – Iceland, Norway, mountains (teal shadows, orange skin)
- `moody_dark` – night scenes, jungles (crushed blacks, high contrast)
- `bright_airy` – beaches, Europe cities (lifted whites, soft pastels)
- `cinematic` – default universal preset (slight S-curve, vignette, mild desaturation)

**Text Overlay Style:**
- Location title: uppercase, bold, white, centered, 80–100px
- Subtitle (optional): regular weight, 40px, 60% opacity
- Appear: fade in at 0.5s, hold, fade out at clip end
- Position: lower third (1400–1600px from top on 1920 tall canvas)
- Drop shadow: 3px offset, 70% black

**Audio:**
- Fade music in over 1s at start
- Duck music to 20% if original clip has loud audio
- Fade out music over 2s before end

---

## Execution Workflow

When the user provides a footage folder, follow this sequence:

### Step 1: Scan and Inventory

```bash
python3 /path/to/scripts/scan_footage.py --root <project_root>
```

Outputs a JSON inventory: clip paths, durations, resolutions, has_audio flags.

### Step 2: Determine Mood & Preset

Infer the mood from the destination folder name:
- `bali`, `mexico`, `marrakech`, `portugal`, `italy` → `warm_golden`
- `iceland`, `norway`, `patagonia`, `alaska`, `swiss` → `cool_teal`
- `tokyo`, `ny`, `berlin`, `singapore` (night/urban) → `moody_dark`
- `santorini`, `maldives`, `amalfi`, `greece` → `bright_airy`
- anything else → `cinematic` (safe default)

Ask the user to confirm or override.

### Step 3: Select Music

Randomly select one track from `_music/`. If `_music/` is empty or missing, proceed without music and notify the user.

### Step 4: Generate the Reel

Run the main editor script:

```bash
python3 /path/to/scripts/build_reel.py \
  --clips-dir <destination_folder> \
  --music <selected_track> \
  --font <font_path> \
  --preset <mood_preset> \
  --location-name "<Destination Name>" \
  --output <output_path>
```

### Step 5: Present Output

Use `present_files` to deliver the final `.mp4` to the user.
Report: duration, clips used, music track, preset applied, any clips skipped.

---

## Scripts

See `scripts/scan_footage.py` — scans project root, returns JSON inventory.
See `scripts/build_reel.py` — main editor: clips → reel pipeline.

Read both scripts fully before executing. They are self-contained and handle all ffmpeg subprocess calls.

---

## Error Handling

| Issue | Action |
|---|---|
| Clip has no video stream | Skip it, log warning |
| Clip is portrait but low-res | Upscale with padding |
| Clip is landscape | Crop to 9:16 (center crop by default) |
| `_music/` missing | Build reel silently, note "no music" in report |
| `_fonts/` missing | Fall back to ffmpeg built-in font (DejaVu) |
| Clip shorter than 1s | Skip it |
| Total footage under 10s | Warn user, use all clips, extend with slow-mo |

---

## Output Naming

`<destination-name>_reel_<YYYYMMDD>.mp4`
Example: `bali_reel_20250414.mp4`

---

## Multi-Destination Mode

If the root folder contains multiple destination subfolders, ask the user:
> "I found [N] destinations: [list]. Should I edit all of them, or start with one?"

Process them sequentially, one reel per destination.
