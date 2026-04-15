#!/usr/bin/env python3
import argparse
import subprocess
import glob
import os

def run(cmd):
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clips-dir", required=True)
    parser.add_argument("--music")
    parser.add_argument("--font")
    parser.add_argument("--preset")
    parser.add_argument("--location-name")
    parser.add_argument("--output", required=True)
    parser.add_argument("--target-duration", type=int, default=30)
    args = parser.parse_args()

    files = glob.glob(os.path.join(args.clips_dir, "*.mp4")) + glob.glob(os.path.join(args.clips_dir, "*.MOV"))
    files = sorted(files)[:6] # take up to 6 clips
    if not files:
        print("No files found!")
        return

    filter_complex = ""
    for i, f in enumerate(files):
        filter_complex += f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,trim=start=0:duration=3,setpts=PTS-STARTPTS[v{i}];"
    
    concat_inputs = "".join(f"[v{i}]" for i in range(len(files)))
    filter_complex += f"{concat_inputs}concat=n={len(files)}:v=1:a=0[vout]"

    cmd = ["ffmpeg", "-y"]
    for f in files:
        cmd += ["-i", f]
    
    if args.music:
        cmd += ["-i", args.music]

    cmd += ["-filter_complex", filter_complex]
    cmd += ["-map", "[vout]"]
    
    if args.music:
        cmd += ["-map", f"{len(files)}:a"]
    
    cmd += ["-c:v", "libx264", "-c:a", "aac", "-t", str(len(files)*3), args.output]
    run(cmd)

if __name__ == "__main__":
    main()
