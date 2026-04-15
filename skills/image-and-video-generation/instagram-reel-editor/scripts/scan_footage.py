#!/usr/bin/env python3
"""
scan_footage.py — Scans a travel project root and returns a JSON inventory
of all clips, music tracks, and fonts found.

Usage:
    python3 scan_footage.py --root /path/to/travel-project
    python3 scan_footage.py --root /path/to/travel-project --destination bali
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

VIDEO_EXTS = {".mp4", ".mov", ".avi", ".mkv", ".MP4", ".MOV", ".AVI", ".MKV"}
AUDIO_EXTS = {".mp3", ".wav", ".aac", ".m4a", ".ogg"}
FONT_EXTS  = {".ttf", ".otf", ".TTF", ".OTF"}


def probe_clip(path: Path) -> dict:
    """Use ffprobe to get clip metadata."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_streams", "-show_format",
        str(path)
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        data = json.loads(result.stdout)
    except Exception as e:
        return {"error": str(e), "path": str(path)}

    info = {
        "path": str(path),
        "filename": path.name,
        "duration": float(data.get("format", {}).get("duration", 0)),
        "size_mb": round(int(data.get("format", {}).get("size", 0)) / 1024 / 1024, 2),
        "has_video": False,
        "has_audio": False,
        "width": None,
        "height": None,
        "fps": None,
        "is_portrait": None,
        "is_usable": False,
    }

    for stream in data.get("streams", []):
        if stream.get("codec_type") == "video" and not info["has_video"]:
            info["has_video"] = True
            info["width"] = stream.get("width")
            info["height"] = stream.get("height")
            # Parse fps from avg_frame_rate like "30000/1001"
            fps_str = stream.get("avg_frame_rate", "0/1")
            try:
                num, den = fps_str.split("/")
                info["fps"] = round(int(num) / int(den), 2) if int(den) > 0 else 0
            except Exception:
                info["fps"] = 0
            if info["width"] and info["height"]:
                info["is_portrait"] = info["height"] > info["width"]
        if stream.get("codec_type") == "audio":
            info["has_audio"] = True

    info["is_usable"] = info["has_video"] and info["duration"] >= 1.0
    return info


def scan_root(root: Path, destination: str = None) -> dict:
    root = root.resolve()
    if not root.exists():
        print(f"ERROR: Root path does not exist: {root}", file=sys.stderr)
        sys.exit(1)

    inventory = {
        "root": str(root),
        "destinations": {},
        "music": [],
        "fonts": [],
        "warnings": []
    }

    # Scan music
    music_dir = root / "_music"
    if music_dir.exists():
        for f in sorted(music_dir.iterdir()):
            if f.suffix.lower() in {".mp3", ".wav", ".aac", ".m4a", ".ogg"}:
                inventory["music"].append(str(f))
    else:
        inventory["warnings"].append("No _music/ folder found — reels will have no background music.")

    # Scan fonts
    font_dir = root / "_fonts"
    if font_dir.exists():
        for f in sorted(font_dir.iterdir()):
            if f.suffix in FONT_EXTS:
                inventory["fonts"].append(str(f))
    else:
        inventory["warnings"].append("No _fonts/ folder found — will fall back to system font.")

    # Scan destinations
    for item in sorted(root.iterdir()):
        if not item.is_dir():
            continue
        if item.name.startswith("_"):
            continue  # skip _music, _fonts, _output etc.
        if destination and item.name.lower() != destination.lower():
            continue

        clips = []
        for f in sorted(item.rglob("*")):
            if f.suffix in VIDEO_EXTS:
                clip_info = probe_clip(f)
                clips.append(clip_info)

        usable = [c for c in clips if c.get("is_usable")]
        skipped = [c for c in clips if not c.get("is_usable")]

        inventory["destinations"][item.name] = {
            "folder": str(item),
            "clips": clips,
            "usable_count": len(usable),
            "skipped_count": len(skipped),
            "total_usable_duration": round(sum(c["duration"] for c in usable), 2),
        }

        if len(usable) == 0:
            inventory["warnings"].append(
                f"Destination '{item.name}' has no usable clips — will be skipped."
            )

    return inventory


def main():
    parser = argparse.ArgumentParser(description="Scan travel footage project root.")
    parser.add_argument("--root", required=True, help="Path to travel project root folder")
    parser.add_argument("--destination", default=None, help="Scan only this destination subfolder")
    args = parser.parse_args()

    root = Path(args.root)
    inventory = scan_root(root, destination=args.destination)

    # Pretty print summary to stderr
    print(f"\n=== Footage Inventory: {root.name} ===", file=sys.stderr)
    print(f"Music tracks: {len(inventory['music'])}", file=sys.stderr)
    print(f"Fonts: {len(inventory['fonts'])}", file=sys.stderr)
    print(f"Destinations: {len(inventory['destinations'])}", file=sys.stderr)
    for dest, data in inventory["destinations"].items():
        print(f"  [{dest}] {data['usable_count']} usable clips, {data['total_usable_duration']:.1f}s total", file=sys.stderr)
    for w in inventory["warnings"]:
        print(f"  ⚠ {w}", file=sys.stderr)

    # JSON to stdout for piping
    print(json.dumps(inventory, indent=2))


if __name__ == "__main__":
    main()
