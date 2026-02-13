---
name: eigent-blog
description: Create and manage blog posts for the Eigent website. Use when the user wants to add, edit, or work with blog posts in the Eigent repository. Triggers include requests to create blog posts, add content to the blog, edit existing posts, generate blog post templates, or work with blog frontmatter and metadata. Also use when asked about blog post structure, formatting requirements, or asset organization.
---

# Eigent Blog Post Management

Create and manage blog posts for the Eigent website with proper frontmatter, directory structure, and asset organization.

## Overview

Blog posts are stored as Markdown (`.md`) or MDX (`.mdx`) files in `view/public/blog/posts/`. Each post requires frontmatter metadata and follows specific organizational patterns.

## Quick Start

### Creating a New Blog Post

Use the generate_post.py script to create a properly formatted template:

```bash
python scripts/generate_post.py "Your Blog Title" \
  --category "Tutorial" \
  --author "Author Name" \
  --featured
```

Or create manually with minimum required frontmatter:

```yaml
---
title: "Your Blog Post Title"
date: "2025-01-15"
---
```

### File Location and URL Mapping

- **Create in**: `view/public/blog/posts/your-post-slug.mdx`
- **Filename**: Use kebab-case (e.g., `getting-started.mdx`)
- **URL**: `/blog/your-post-slug` (filename without extension)

## Frontmatter Structure

### Required Fields
- `title` (string): Blog post title
- `date` (string): Publication date in YYYY-MM-DD format

### Common Optional Fields
- `subtitle`: Subtitle below title
- `author`: Author name (default: "Eigent")
- `authorprofile`: Path to author image (e.g., `/blog/author/name.png`)
- `role`: Author's role (default: "Author")
- `description`: SEO description (150-160 chars recommended)
- `keywords`: Array or comma-separated string
- `toc`: Enable table of contents (default: true)
- `thumbnail`: Path to thumbnail (e.g., `/blog/thumbnail/post.png`)
- `featured`: Mark as featured (default: false)
- `category`: Category label (e.g., "Tutorial", "Case Study")

See [frontmatter-guide.md](references/frontmatter-guide.md) for complete field specifications and examples.

## Directory Structure

```
view/public/blog/
├── posts/         # .md/.mdx files
├── thumbnail/     # 1200x630px thumbnails
├── author/        # 200x200px author profiles
└── [assets]/      # Other images/videos
```

See [directory-structure.md](references/directory-structure.md) for detailed organization guidelines.

## Content Guidelines

### Markdown Features
- Use standard Markdown syntax
- Headings automatically included in TOC (if enabled)
- Code blocks support syntax highlighting
- Images: `![Alt](/blog/image.png)`
- Links: `[Text](https://url.com)`

### Image Assets
- **Thumbnails**: 1200x630px in `thumbnail/`
- **Author images**: 200x200px in `author/` (displayed circular)
- **Content images**: Place in `/blog/` with descriptive names
- **Reference with absolute paths**: `/blog/asset-name.png`

### Best Practices
1. Use kebab-case for all filenames
2. Write compelling descriptions (150-160 chars for SEO)
3. Include relevant keywords for discoverability
4. Use consistent category names across posts
5. Feature only best/most important posts
6. Optimize images before uploading
7. Structure content with clear headings

## Workflow Steps

When creating a blog post:

1. **Generate template** using generate_post.py script OR create file manually
2. **Add frontmatter** with required fields (title, date) and relevant optional fields
3. **Write content** using Markdown/MDX syntax
4. **Add images**:
   - Create thumbnail (1200x630px) in `thumbnail/`
   - Add author profile (200x200px) in `author/` if needed
   - Place content images in `/blog/`
5. **Save to** `view/public/blog/posts/[slug].mdx`
6. **Verify** frontmatter formatting and image paths
7. **Optional: Open a PR**:
   - Create a branch (for example: `codex/blog-[slug]`)
   - Commit the blog and asset changes with a clear message
   - Push the branch and open a pull request for review

## Common Issues

### Post Not Appearing
- Check file is in `view/public/blog/posts/`
- Verify frontmatter YAML syntax (between `---`)
- Ensure required fields present (title, date)

### Images Not Loading
- Verify paths start with `/blog/`
- Check files exist in correct directory
- Ensure exact filename match (case-sensitive)

### TOC Not Showing
- Set `toc: true` in frontmatter (or omit, as true is default)
- Ensure post has headings (`#`, `##`, etc.)

## Scripts

- **generate_post.py**: Generate blog post templates with proper structure
  - Automatically creates frontmatter with defaults
  - Generates URL-friendly slugs
  - Supports custom categories, authors, featured status

## Git Handoff (Optional)

Use this when the user asks to ship changes via GitHub:

1. Create a branch with prefix `codex/`.
2. Stage only intended blog-related files.
3. Commit with a clear summary.
4. Open a PR with:
   - What post was added/updated
   - Which assets were added/updated
   - Any follow-up items (if applicable)

## References

- **frontmatter-guide.md**: Complete frontmatter field specifications
- **directory-structure.md**: Asset organization and path conventions
