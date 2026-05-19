#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


PATTERNS = {
    "failures": re.compile(
        r"failed|failure|assertionerror|error|exception|traceback|oom|out of memory|timeout",
        re.IGNORECASE,
    ),
    "passes": re.compile(r"passed|success|completed|finished|saved checkpoint", re.IGNORECASE),
    "metrics": re.compile(
        r"loss|accuracy|iteration[-_ ]?time|throughput|tokens/s|samples/s|global batch|"
        r"consumed samples|nan iterations|skipped iterations|memory|mfu|tflops",
        re.IGNORECASE,
    ),
    "config": re.compile(r"batch|seq|seed|lr|learning rate|checkpoint|resume|parallel", re.IGNORECASE),
}


def read_text(path: Path) -> str:
    return path.read_text(errors="ignore")


def window(lines: list[str], idx: int, radius: int = 3) -> list[str]:
    start = max(0, idx - radius)
    end = min(len(lines), idx + radius + 1)
    return lines[start:end]


def scan_log(path: Path) -> dict:
    lines = read_text(path).splitlines()
    result = {"path": str(path), "line_count": len(lines), "matches": {}}
    for name, pattern in PATTERNS.items():
        hits = []
        for idx, line in enumerate(lines):
            if pattern.search(line):
                hits.append(
                    {
                        "line": idx + 1,
                        "text": line[-1200:],
                        "context": window(lines, idx),
                    }
                )
            if len(hits) >= 80:
                break
        result["matches"][name] = hits
    return result


def scan_repo(repo: Path) -> dict:
    candidates = []
    names = [
        "model_config.yaml",
        "golden_values",
        "common.py",
        "test_",
        "train",
        "eval",
        "metric",
        "config",
    ]
    for path in repo.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(repo)
        if any(part in {".git", "__pycache__", "node_modules"} for part in rel.parts):
            continue
        rel_s = rel.as_posix()
        if any(name in rel_s for name in names):
            candidates.append(rel_s)
        if len(candidates) >= 300:
            break
    return {
        "repo": str(repo),
        "candidate_files": candidates,
        "has_tests": (repo / "tests").exists(),
        "has_pyproject": (repo / "pyproject.toml").exists(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--logs", nargs="*", default=[])
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    logs = []
    for raw in args.logs:
        p = Path(raw)
        if p.is_dir():
            logs.extend(sorted(p.glob("*.log")))
        elif p.exists():
            logs.append(p.resolve())

    data = {
        "repo_summary": scan_repo(repo),
        "logs": [scan_log(p) for p in logs],
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2))
    print(out)


if __name__ == "__main__":
    main()
