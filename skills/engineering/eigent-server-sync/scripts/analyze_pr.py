#!/usr/bin/env python3
"""
Analyze a GitHub PR from eigent/server/ and generate a sync plan for eigent_server.

Usage:
    python analyze_pr.py <PR_URL_OR_NUMBER> [--output plan.json]

Examples:
    python analyze_pr.py 123
    python analyze_pr.py https://github.com/eigent-ai/eigent/pull/123
    python analyze_pr.py 123 --output sync_plan.json
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
import urllib.error
from dataclasses import dataclass, asdict, field
from enum import Enum
from pathlib import Path
from typing import Optional


class SyncStatus(Enum):
    SYNC = "sync"           # File should be synced
    SKIP = "skip"           # File outside server/ directory
    CREATE = "create"       # New file to create in target


@dataclass
class FileMapping:
    source_path: str
    target_path: Optional[str]
    status: SyncStatus
    change_type: str  # added, modified, deleted, renamed


@dataclass
class SyncPlan:
    pr_number: int
    pr_title: str
    pr_url: str
    pr_author: str
    pr_body: str
    base_branch: str
    head_branch: str
    source_repo: str
    target_repo: str
    file_mappings: list = field(default_factory=list)
    sync_required: bool = False
    file_count: int = 0
    summary: str = ""


# Source repository configuration
SOURCE_REPO = "eigent-ai/eigent"
TARGET_REPO = "eigent-ai/eigent_server"
SERVER_PREFIX = "server/"

# GitHub API base URL
GITHUB_API_BASE = "https://api.github.com"


def check_gh_cli_available() -> bool:
    """Check if gh CLI is installed and available."""
    try:
        result = subprocess.run(
            ["gh", "--version"],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def check_gh_auth() -> bool:
    """Check if gh CLI is authenticated."""
    try:
        result = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def run_gh_command(args: list, check: bool = True) -> Optional[dict]:
    """Run a gh CLI command and return JSON output."""
    try:
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True,
            text=True,
            check=check
        )
        if result.stdout:
            return json.loads(result.stdout)
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error running gh command: {e.stderr}", file=sys.stderr)
        if check:
            sys.exit(1)
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing gh output: {e}", file=sys.stderr)
        if check:
            sys.exit(1)
        return None
    except FileNotFoundError:
        return None


def github_api_request(endpoint: str, token: Optional[str] = None) -> Optional[dict]:
    """Make a request to the GitHub API."""
    url = f"{GITHUB_API_BASE}{endpoint}"

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "eigent-server-sync/1.0"
    }

    # Add authentication if token is provided
    if token:
        headers["Authorization"] = f"token {token}"
    else:
        # Try to get token from environment
        env_token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if env_token:
            headers["Authorization"] = f"token {env_token}"

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: Resource not found (404): {url}", file=sys.stderr)
        elif e.code == 403:
            print(f"Error: Rate limit exceeded or access forbidden (403)", file=sys.stderr)
            print("Hint: Set GITHUB_TOKEN environment variable for higher rate limits", file=sys.stderr)
        else:
            print(f"Error: HTTP {e.code}: {e.reason}", file=sys.stderr)
        return None
    except urllib.error.URLError as e:
        print(f"Error: Network error: {e.reason}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON response: {e}", file=sys.stderr)
        return None


def fetch_pr_via_gh_cli(pr_number: int) -> Optional[dict]:
    """Fetch PR data using gh CLI."""
    return run_gh_command([
        "pr", "view", str(pr_number),
        "--repo", SOURCE_REPO,
        "--json", "title,body,files,baseRefName,headRefName,author,url"
    ])


def fetch_pr_via_api(pr_number: int) -> Optional[dict]:
    """Fetch PR data using GitHub API directly."""
    # Fetch PR metadata
    pr_endpoint = f"/repos/{SOURCE_REPO}/pulls/{pr_number}"
    pr_data = github_api_request(pr_endpoint)

    if not pr_data:
        return None

    # Fetch PR files (may need pagination for large PRs)
    files_endpoint = f"/repos/{SOURCE_REPO}/pulls/{pr_number}/files"
    files_data = github_api_request(files_endpoint)

    if not files_data:
        return None

    # Combine into gh-compatible format
    return {
        "title": pr_data.get("title", ""),
        "body": pr_data.get("body", ""),
        "baseRefName": pr_data.get("base", {}).get("ref", "main"),
        "headRefName": pr_data.get("head", {}).get("ref", ""),
        "author": {"login": pr_data.get("user", {}).get("login", "unknown")},
        "url": pr_data.get("html_url", ""),
        "files": [
            {
                "path": f.get("filename", ""),
                "additions": f.get("additions", 0),
                "deletions": f.get("deletions", 0),
                "status": f.get("status", "modified")
            }
            for f in files_data
        ]
    }


def extract_pr_number(input_str: str) -> int:
    """Extract PR number from URL or direct number."""
    # Try matching URL pattern
    url_match = re.search(r"github\.com/[^/]+/[^/]+/pull/(\d+)", input_str)
    if url_match:
        return int(url_match.group(1))

    # Try parsing as direct number
    try:
        return int(input_str.strip())
    except ValueError:
        print(f"Invalid PR reference: {input_str}", file=sys.stderr)
        sys.exit(1)


def map_file(source_path: str, status: str = "modified") -> FileMapping:
    """Map an eigent file path to eigent_server equivalent."""
    # Normalize path
    normalized = source_path.replace("\\", "/")

    # Check if file is in server/ directory
    if not normalized.startswith(SERVER_PREFIX):
        return FileMapping(
            source_path=source_path,
            target_path=None,
            status=SyncStatus.SKIP,
            change_type=status
        )

    # Map server/* to server/* (same path structure)
    return FileMapping(
        source_path=source_path,
        target_path=normalized,
        status=SyncStatus.SYNC,
        change_type=status
    )


def analyze_pr(pr_ref: str, use_api: bool = False, token: Optional[str] = None) -> SyncPlan:
    """Analyze a PR and create a sync plan."""
    pr_number = extract_pr_number(pr_ref)

    # Fetch PR data
    pr_data = None
    method_used = ""

    if use_api or not check_gh_cli_available():
        print("Using GitHub API...", file=sys.stderr)
        pr_data = fetch_pr_via_api(pr_number)
        method_used = "API"
    else:
        print("Using gh CLI...", file=sys.stderr)
        pr_data = fetch_pr_via_gh_cli(pr_number)
        method_used = "CLI"

    if not pr_data:
        print(f"Could not fetch PR #{pr_number}", file=sys.stderr)
        sys.exit(1)

    # Map all changed files
    file_mappings = []
    sync_count = 0

    for file_info in pr_data.get("files", []):
        source_path = file_info.get("path", file_info.get("filename", ""))

        # Determine change type
        file_status = file_info.get("status", "modified")
        if file_status == "added":
            change_type = "added"
        elif file_status == "removed":
            change_type = "deleted"
        elif file_status == "renamed":
            change_type = "renamed"
        else:
            # Fallback: infer from additions/deletions
            additions = file_info.get("additions", 0)
            deletions = file_info.get("deletions", 0)
            if additions > 0 and deletions == 0:
                change_type = "added"
            elif deletions > 0 and additions == 0:
                change_type = "deleted"
            else:
                change_type = "modified"

        mapping = map_file(source_path, change_type)
        file_mappings.append(asdict(mapping))

        if mapping.status == SyncStatus.SYNC:
            sync_count += 1

    # Create summary
    if sync_count == 0:
        summary = "No server files found in this PR. Nothing to sync."
    elif sync_count == 1:
        synced = [m['source_path'] for m in file_mappings if m['status'] == SyncStatus.SYNC.value]
        summary = f"1 server file to sync: {synced[0] if synced else ''}"
    else:
        summary = f"{sync_count} server files to sync"

    return SyncPlan(
        pr_number=pr_number,
        pr_title=pr_data.get("title", ""),
        pr_url=pr_data.get("url", pr_data.get("html_url", "")),
        pr_author=pr_data.get("author", {}).get("login", "unknown"),
        pr_body=pr_data.get("body", ""),
        base_branch=pr_data.get("baseRefName", "main"),
        head_branch=pr_data.get("headRefName", ""),
        source_repo=SOURCE_REPO,
        target_repo=TARGET_REPO,
        file_mappings=file_mappings,
        sync_required=sync_count > 0,
        file_count=sync_count,
        summary=summary
    )


def format_text_output(plan: SyncPlan) -> str:
    """Format sync plan as human-readable text."""
    lines = [
        "=" * 60,
        f"PR #{plan.pr_number}: {plan.pr_title}",
        "=" * 60,
        f"URL: {plan.pr_url}",
        f"Author: {plan.pr_author}",
        f"Branch: {plan.head_branch} -> {plan.base_branch}",
        "",
        f"Source: {plan.source_repo}",
        f"Target: {plan.target_repo}",
        "",
        f"Sync Required: {'Yes' if plan.sync_required else 'No'}",
        f"Files to Sync: {plan.file_count}",
        "",
        plan.summary,
        "",
    ]

    if plan.file_mappings:
        # Handle both Enum objects and string values
        def is_sync(m):
            status = m["status"]
            return status == SyncStatus.SYNC or status == SyncStatus.SYNC.value

        def is_skip(m):
            status = m["status"]
            return status == SyncStatus.SKIP or status == SyncStatus.SKIP.value

        sync_files = [m for m in plan.file_mappings if is_sync(m)]
        skip_files = [m for m in plan.file_mappings if is_skip(m)]

        if sync_files:
            lines.append("FILES TO SYNC:")
            lines.append("-" * 40)
            for fm in sync_files:
                change_icon = {"added": "+", "modified": "~", "deleted": "-", "renamed": "R"}.get(fm["change_type"], "?")
                lines.append(f"  [{change_icon}] {fm['source_path']}")
                if fm["target_path"]:
                    lines.append(f"      -> {fm['target_path']}")
            lines.append("")

        if skip_files:
            lines.append(f"SKIPPED ({len(skip_files)} files outside server/):")
            lines.append("-" * 40)
            for fm in skip_files[:5]:  # Show first 5
                lines.append(f"  [x] {fm['source_path']}")
            if len(skip_files) > 5:
                lines.append(f"  ... and {len(skip_files) - 5} more")
            lines.append("")

    lines.append("=" * 60)
    lines.append("Next steps:")
    if plan.sync_required:
        lines.append(f"  1. Review the files to sync")
        lines.append(f"  2. Create feature branch: sync/eigent-pr-{plan.pr_number}")
        lines.append("  3. Apply changes to eigent_server")
        lines.append("  4. Create PR in eigent_server")
    else:
        lines.append("  No sync needed - PR contains no server/ files.")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze an eigent PR for eigent_server sync requirements"
    )
    parser.add_argument(
        "pr_ref",
        help="PR URL or number (e.g., https://github.com/eigent-ai/eigent/pull/123 or 123)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file for sync plan (JSON format)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)"
    )
    parser.add_argument(
        "--api",
        action="store_true",
        help="Force using GitHub API instead of gh CLI"
    )
    parser.add_argument(
        "--token",
        help="GitHub personal access token (or set GITHUB_TOKEN env var)"
    )

    args = parser.parse_args()

    # Determine which method to use
    use_api = args.api

    if not use_api and not check_gh_cli_available():
        print("gh CLI not found, falling back to GitHub API...", file=sys.stderr)
        use_api = True

    if not use_api and not check_gh_auth():
        print("gh CLI not authenticated, falling back to GitHub API...", file=sys.stderr)
        print("Hint: Run 'gh auth login' or set GITHUB_TOKEN for higher rate limits", file=sys.stderr)
        use_api = True

    # Analyze PR
    plan = analyze_pr(args.pr_ref, use_api=use_api, token=args.token)
    plan_dict = asdict(plan)

    # Convert enum values to strings for JSON serialization
    for fm in plan_dict["file_mappings"]:
        fm["status"] = fm["status"].value if hasattr(fm["status"], "value") else fm["status"]

    # Output
    if args.format == "json":
        output = json.dumps(plan_dict, indent=2)
    else:
        output = format_text_output(plan)

    if args.output:
        Path(args.output).write_text(json.dumps(plan_dict, indent=2))
        print(f"Sync plan saved to {args.output}")
        print(output)
    else:
        print(output)


if __name__ == "__main__":
    main()