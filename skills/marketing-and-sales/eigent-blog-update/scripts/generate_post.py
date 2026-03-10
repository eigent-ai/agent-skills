#!/usr/bin/env python3
"""
Generate a new blog post template with proper frontmatter structure.

Usage:
    python generate_post.py "Blog Post Title" [--slug custom-slug] [--featured] [--category "Category"]
"""

import argparse
import re
from datetime import datetime
from pathlib import Path


def slugify(text):
    """Convert title to URL-safe slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def generate_post_template(
    title,
    slug=None,
    featured=False,
    category=None,
    subtitle=None,
    author=None,
    output_dir=None
):
    """Generate a blog post template with frontmatter."""
    
    # Generate slug from title if not provided
    if not slug:
        slug = slugify(title)
    
    # Get current date
    date = datetime.now().strftime("%Y-%m-%d")
    
    # Build frontmatter
    frontmatter_lines = [
        "---",
        f'title: "{title}"'
    ]
    
    if subtitle:
        frontmatter_lines.append(f'subtitle: "{subtitle}"')
    
    frontmatter_lines.append(f'date: "{date}"')
    
    if author:
        frontmatter_lines.append(f'author: "{author}"')
        frontmatter_lines.append(f'authorprofile: "/blog/author/{slugify(author)}.png"')
        frontmatter_lines.append('role: "Author"')
    
    frontmatter_lines.append('description: "Add a compelling description here (150-160 characters for SEO)"')
    frontmatter_lines.append('keywords: ["keyword1", "keyword2", "keyword3"]')
    frontmatter_lines.append('toc: true')
    frontmatter_lines.append(f'thumbnail: "/blog/thumbnail/{slug}.png"')
    frontmatter_lines.append(f'featured: {str(featured).lower()}')
    
    if category:
        frontmatter_lines.append(f'category: "{category}"')
    
    frontmatter_lines.append("---")
    
    # Build content template
    content_lines = [
        "",
        "# Introduction",
        "",
        "Start your blog post here...",
        "",
        "## Section 1",
        "",
        "Add your content.",
        "",
        "### Subsection",
        "",
        "More details here.",
        "",
        "## Section 2",
        "",
        "Continue your post.",
        "",
        "## Conclusion",
        "",
        "Wrap up your thoughts.",
        ""
    ]
    
    # Combine frontmatter and content
    full_template = "\n".join(frontmatter_lines + content_lines)
    
    # Determine output path
    if output_dir:
        output_path = Path(output_dir) / f"{slug}.mdx"
    else:
        output_path = Path(f"{slug}.mdx")
    
    # Write file
    output_path.write_text(full_template)
    
    return output_path, slug


def main():
    parser = argparse.ArgumentParser(
        description="Generate a new Eigent blog post template"
    )
    parser.add_argument(
        "title",
        help="Blog post title"
    )
    parser.add_argument(
        "--slug",
        help="Custom URL slug (defaults to slugified title)"
    )
    parser.add_argument(
        "--featured",
        action="store_true",
        help="Mark post as featured"
    )
    parser.add_argument(
        "--category",
        help="Post category (e.g., 'Tutorial', 'Case Study')"
    )
    parser.add_argument(
        "--subtitle",
        help="Post subtitle"
    )
    parser.add_argument(
        "--author",
        help="Author name"
    )
    parser.add_argument(
        "--output-dir",
        help="Output directory (defaults to current directory)"
    )
    
    args = parser.parse_args()
    
    output_path, slug = generate_post_template(
        title=args.title,
        slug=args.slug,
        featured=args.featured,
        category=args.category,
        subtitle=args.subtitle,
        author=args.author,
        output_dir=args.output_dir
    )
    
    print(f"✅ Blog post template created: {output_path}")
    print(f"📝 Title: {args.title}")
    print(f"🔗 URL slug: {slug}")
    print(f"📍 URL will be: /blog/{slug}")
    print("\n📋 Next steps:")
    print("1. Update the description in the frontmatter")
    print("2. Add relevant keywords")
    print("3. Create thumbnail image at /blog/thumbnail/{}.png".format(slug))
    if args.author:
        print("4. Create author image at /blog/author/{}.png".format(slugify(args.author)))
    print("5. Write your content below the frontmatter")
    print("6. Move file to view/public/blog/posts/")


if __name__ == "__main__":
    main()