#!/usr/bin/env python3
"""
Generate a new usecase JSON file with proper structure.

Usage:
    python generate_usecase.py "Usecase Title" [--featured] [--keywords keyword1,keyword2] [--replay-url URL] [--upload-date YYYY-MM-DD]
"""

import argparse
import json
import re
from datetime import date
from pathlib import Path


def slugify(text):
    """Convert title to snake_case ID."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '_', text)
    return text.strip('_')


def generate_usecase_json(
    title,
    usecase_id=None,
    prompt=None,
    description=None,
    replay_url=None,
    upload_date=None,
    featured=False,
    keywords=None,
    meta_description=None,
    output_dir=None
):
    """Generate a usecase JSON file with proper structure."""
    
    # Generate ID from title if not provided
    if not usecase_id:
        usecase_id = slugify(title)
    
    # Generate default prompt if not provided
    if not prompt:
        prompt = f"Brief description for {title}"
    
    # Generate default description if not provided
    if not description:
        description = f"Full detailed description of {title}. Explain what this usecase does and how it helps users."
    
    # Generate default keywords if not provided
    if not keywords:
        keywords = ["usecase", "automation", "workflow"]
    
    # Generate default meta description if not provided
    if not meta_description:
        meta_description = f"{title} - Automate workflows with Eigent's multi-agent system."

    # Generate upload date if not provided
    if not upload_date:
        upload_date = date.today().isoformat()

    # Default replay URL to empty string when omitted
    if replay_url is None:
        replay_url = ""

    # Build usecase JSON structure
    usecase_data = {
        "id": usecase_id,
        "title": title,
        "prompt": prompt,
        "description": description,
        "image": f"/gallery/{usecase_id}.png",
        "videoSrc": f"/gallery/{usecase_id}.mp4",
        "videoPoster": f"/gallery/{usecase_id}.png",
        "videoTitle": title,
        "replayUrl": replay_url,
        "uploadDate": upload_date,
        "featured": featured,
        "keywords": keywords,
        "metaDescription": meta_description
    }
    
    # Determine output path
    if output_dir:
        output_path = Path(output_dir) / f"{usecase_id}.json"
    else:
        output_path = Path(f"{usecase_id}.json")
    
    # Write JSON file with pretty formatting
    with open(output_path, 'w') as f:
        json.dump(usecase_data, f, indent=2, ensure_ascii=False)
        f.write('\n')  # Add trailing newline
    
    return output_path, usecase_id


def main():
    parser = argparse.ArgumentParser(
        description="Generate a new Eigent usecase JSON file"
    )
    parser.add_argument(
        "title",
        help="Usecase title"
    )
    parser.add_argument(
        "--id",
        dest="usecase_id",
        help="Custom ID (defaults to snake_case version of title)"
    )
    parser.add_argument(
        "--prompt",
        help="Short prompt description for card display (50-100 chars)"
    )
    parser.add_argument(
        "--description",
        help="Full detailed description"
    )
    parser.add_argument(
        "--replay-url",
        dest="replay_url",
        help="Replay URL for the usecase demo"
    )
    parser.add_argument(
        "--upload-date",
        dest="upload_date",
        help="Upload date in YYYY-MM-DD format (defaults to today)"
    )
    parser.add_argument(
        "--featured",
        action="store_true",
        help="Mark usecase as featured"
    )
    parser.add_argument(
        "--keywords",
        help="Comma-separated keywords (e.g., 'finance,reporting,automation')"
    )
    parser.add_argument(
        "--meta-description",
        dest="meta_description",
        help="SEO meta description (150-160 characters)"
    )
    parser.add_argument(
        "--output-dir",
        help="Output directory (defaults to current directory)"
    )
    
    args = parser.parse_args()
    
    # Parse keywords if provided
    keywords = None
    if args.keywords:
        keywords = [k.strip() for k in args.keywords.split(',')]

    # Validate upload date format if provided
    if args.upload_date:
        try:
            date.fromisoformat(args.upload_date)
        except ValueError:
            parser.error("--upload-date must be in YYYY-MM-DD format")

    output_path, usecase_id = generate_usecase_json(
        title=args.title,
        usecase_id=args.usecase_id,
        prompt=args.prompt,
        description=args.description,
        replay_url=args.replay_url,
        upload_date=args.upload_date,
        featured=args.featured,
        keywords=keywords,
        meta_description=args.meta_description,
        output_dir=args.output_dir
    )
    
    print(f"✅ Usecase JSON created: {output_path}")
    print(f"📝 Title: {args.title}")
    print(f"🆔 ID: {usecase_id}")
    print(f"🔗 URL will be: /usecases/{usecase_id}")
    print(f"\n📋 Next steps:")
    print(f"1. Edit {output_path} to update prompt and description")
    print(f"2. Create card image: /gallery/{usecase_id}.png (800x600px)")
    print(f"3. Create demo video: /gallery/{usecase_id}.mp4")
    print(f"4. Set video poster: /gallery/{usecase_id}.png (or provide a dedicated poster path)")
    print(f"5. Update keywords and meta description")
    print(f"6. Move file to public/usecase/posts/")


if __name__ == "__main__":
    main()
