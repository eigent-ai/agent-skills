#!/usr/bin/env python3
"""
Ingest an uploaded markdown file into this repository's Mintlify docs tree.

The script:
1) writes/updates docs/<page>.md
2) ensures frontmatter includes title + description
3) optionally updates docs/docs.json navigation
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest markdown into Mintlify docs.")
    parser.add_argument("--source", required=True, help="Path to source markdown file.")
    parser.add_argument(
        "--page",
        required=True,
        help="Doc route without leading slash, e.g. core/new-feature",
    )
    parser.add_argument("--group", required=True, help='Target Mintlify group, e.g. "Core".')
    parser.add_argument(
        "--subgroup",
        help='Optional nested group under pages, e.g. "Models" for Core/Models.',
    )
    parser.add_argument(
        "--insert-after",
        help="Optional page route to insert after, e.g. /core/models/kimi",
    )
    parser.add_argument("--title", help="Optional override title frontmatter.")
    parser.add_argument("--description", help="Optional override description frontmatter.")
    parser.add_argument(
        "--docs-root",
        default="docs",
        help="Docs root directory. Defaults to docs.",
    )
    parser.add_argument(
        "--docs-json",
        default="docs/docs.json",
        help="Mintlify docs.json path. Defaults to docs/docs.json.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite destination page if it already exists.",
    )
    parser.add_argument(
        "--no-nav",
        action="store_true",
        help="Skip navigation update in docs.json.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned changes without writing files.",
    )
    return parser.parse_args()


def quote_yaml_scalar(value: str) -> str:
    safe = value.replace('"', '\\"')
    return f'"{safe}"'


def slug_to_title(slug: str) -> str:
    tail = slug.split("/")[-1]
    return " ".join(part.capitalize() for part in re.split(r"[-_]+", tail) if part)


def derive_title(markdown_body: str, fallback_slug: str) -> str:
    for line in markdown_body.splitlines():
        if line.startswith("# "):
            return line.replace("# ", "", 1).strip()
    return slug_to_title(fallback_slug)


def ensure_frontmatter(markdown_text: str, page: str, title: str | None, description: str | None) -> str:
    desired_title = title or derive_title(markdown_text, page)
    desired_description = description or f"Documentation for {desired_title}."

    if markdown_text.startswith("---\n"):
        end_marker = "\n---\n"
        end_idx = markdown_text.find(end_marker, 4)
        if end_idx != -1:
            frontmatter = markdown_text[4:end_idx]
            body = markdown_text[end_idx + len(end_marker) :]
            lines = frontmatter.splitlines()
            has_title = any(re.match(r"^\s*title\s*:", ln) for ln in lines)
            has_description = any(re.match(r"^\s*description\s*:", ln) for ln in lines)
            if not has_title:
                lines.insert(0, f"title: {quote_yaml_scalar(desired_title)}")
            if not has_description:
                insert_idx = 1 if lines and lines[0].startswith("title:") else 0
                lines.insert(insert_idx, f"description: {quote_yaml_scalar(desired_description)}")
            updated = "\n".join(lines).rstrip()
            return f"---\n{updated}\n---\n{body.lstrip()}"

    header = (
        f"---\n"
        f"title: {quote_yaml_scalar(desired_title)}\n"
        f"description: {quote_yaml_scalar(desired_description)}\n"
        f"---\n\n"
    )
    return header + markdown_text.lstrip()


def add_page_to_target(
    pages: list,
    page_ref: str,
    insert_after: str | None,
) -> tuple[bool, str]:
    if any(isinstance(item, str) and item == page_ref for item in pages):
        return False, f"Navigation entry already exists: {page_ref}"

    if insert_after:
        for idx, item in enumerate(pages):
            if isinstance(item, str) and item == insert_after:
                pages.insert(idx + 1, page_ref)
                return True, f"Inserted {page_ref} after {insert_after}"

    pages.append(page_ref)
    return True, f"Appended {page_ref}"


def update_docs_json(
    docs_json_path: Path,
    group: str,
    subgroup: str | None,
    page_ref: str,
    insert_after: str | None,
) -> str:
    data = json.loads(docs_json_path.read_text(encoding="utf-8"))
    tabs = data.get("navigation", {}).get("tabs", [])
    if not tabs:
        raise ValueError("No navigation.tabs found in docs.json")

    groups = tabs[0].get("groups", [])
    target_group = next((g for g in groups if g.get("group") == group), None)
    if not target_group:
        raise ValueError(f'Group "{group}" not found in docs.json')

    target_pages = target_group.get("pages", [])
    if subgroup:
        subgroup_obj = next(
            (p for p in target_pages if isinstance(p, dict) and p.get("group") == subgroup),
            None,
        )
        if not subgroup_obj:
            raise ValueError(f'Subgroup "{subgroup}" not found inside group "{group}"')
        changed, message = add_page_to_target(subgroup_obj.setdefault("pages", []), page_ref, insert_after)
    else:
        changed, message = add_page_to_target(target_pages, page_ref, insert_after)
        target_group["pages"] = target_pages

    if changed:
        docs_json_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return message


def main() -> int:
    args = parse_args()
    source = Path(args.source).resolve()
    docs_root = Path(args.docs_root).resolve()
    docs_json_path = Path(args.docs_json).resolve()

    if not source.exists():
        print(f"ERROR: source file not found: {source}", file=sys.stderr)
        return 1
    if not source.is_file():
        print(f"ERROR: source is not a file: {source}", file=sys.stderr)
        return 1

    page = args.page.strip().strip("/")
    page_ref = f"/{page}"
    destination = docs_root / f"{page}.md"

    if destination.exists() and not args.overwrite:
        print(
            f"ERROR: destination already exists: {destination}\n"
            "Use --overwrite to replace it.",
            file=sys.stderr,
        )
        return 1

    raw = source.read_text(encoding="utf-8")
    output = ensure_frontmatter(raw, page, args.title, args.description)

    print(f"Source:      {source}")
    print(f"Destination: {destination}")
    print(f"Page ref:    {page_ref}")
    print(f"Group:       {args.group}")
    if args.subgroup:
        print(f"Subgroup:    {args.subgroup}")
    if args.insert_after:
        print(f"Insert after:{args.insert_after}")

    if not args.no_nav and not docs_json_path.exists():
        print(f"ERROR: docs.json not found: {docs_json_path}", file=sys.stderr)
        return 1

    if args.dry_run:
        print("Dry run: no files written.")
        return 0

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(output, encoding="utf-8")
    print("Wrote markdown page.")

    if not args.no_nav:
        msg = update_docs_json(
            docs_json_path=docs_json_path,
            group=args.group,
            subgroup=args.subgroup,
            page_ref=page_ref,
            insert_after=args.insert_after,
        )
        print(f"Updated docs.json: {msg}")
    else:
        print("Skipped docs.json update (--no-nav).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
