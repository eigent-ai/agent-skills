# Eigent Blog Directory Structure

Complete directory structure and asset organization for the Eigent blog system.

## Main Directories

```
view/public/blog/
├── posts/              # Blog post markdown/mdx files
├── thumbnail/          # Thumbnail images for blog posts
├── author/             # Author profile images
└── [other assets]/     # Additional images, videos, etc. for blog posts
```

## Directory Details

### posts/ Directory
- **Purpose**: Store all blog post .md and .mdx files
- **File naming**: Use kebab-case (e.g., `my-blog-post.mdx`)
- **URL mapping**: Filename (without extension) becomes URL slug
  - Example: `my-blog-post.mdx` → `/blog/my-blog-post`

### thumbnail/ Directory
- **Purpose**: Store thumbnail and cover images for blog posts
- **Recommended size**: 1200x630px for optimal display
- **Formats**: PNG, JPG, WebP
- **Naming**: Use descriptive names matching post slugs when possible
- **Reference in frontmatter**: `thumbnail: "/blog/thumbnail/your-image.png"`

### author/ Directory
- **Purpose**: Store author profile images
- **Recommended size**: 200x200px (square, will be displayed as circular)
- **Formats**: PNG, JPG
- **Naming**: Use author name or identifier
- **Reference in frontmatter**: `authorprofile: "/blog/author/author-name.png"`

### Other Assets
- **Location**: Directly in `/blog/` or subdirectories
- **Types**: Images, videos, GIFs, downloadable files
- **Naming**: Include post slug to avoid conflicts (e.g., `getting-started-diagram.png`)
- **Reference in content**: Absolute paths starting with `/blog/`
  - Example: `![Diagram](/blog/getting-started-diagram.png)`

## Path Examples

### Blog Post Files
- `view/public/blog/posts/getting-started.mdx`
- `view/public/blog/posts/advanced-workflows.md`
- `view/public/blog/posts/case-study-company-x.mdx`

### Thumbnail Images
- `view/public/blog/thumbnail/getting-started.png`
- `view/public/blog/thumbnail/advanced-workflows.jpg`
- `view/public/blog/thumbnail/case-study.webp`

### Author Images
- `view/public/blog/author/eigent.png`
- `view/public/blog/author/john-doe.jpg`
- `view/public/blog/author/team.png`

### Content Assets
- `view/public/blog/workflow-diagram.png`
- `view/public/blog/demo-video.mp4`
- `view/public/blog/architecture-overview.svg`

## URL Structure

### Blog Pages
- Blog index: `https://eigent.com/blog`
- Individual post: `https://eigent.com/blog/[slug]`
  - Example: `https://eigent.com/blog/getting-started`

### Asset URLs
All assets use absolute paths starting with `/blog/`:
- Thumbnail: `/blog/thumbnail/image.png`
- Author: `/blog/author/profile.png`
- Content: `/blog/diagram.png`

## Best Practices

1. **Consistent naming**: Use kebab-case for all filenames
2. **Logical organization**: Keep thumbnails in thumbnail/, authors in author/
3. **Descriptive names**: Use names that indicate content/purpose
4. **Avoid conflicts**: Include post slug in asset names when possible
5. **Optimize images**: Compress images before uploading
6. **Case sensitivity**: Remember that URLs are case-sensitive