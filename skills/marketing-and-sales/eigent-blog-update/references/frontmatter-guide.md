# Blog Post Frontmatter Reference

Complete specification for Eigent blog post frontmatter fields.

## Required Fields

### title
- **Type**: string
- **Description**: Main title of the blog post
- **Example**: `"Getting Started with Eigent"`

### date
- **Type**: string
- **Format**: `YYYY-MM-DD`
- **Description**: Publication date
- **Example**: `"2025-01-15"`

## Optional Fields

### subtitle
- **Type**: string
- **Description**: Optional subtitle displayed below the title
- **Example**: `"A comprehensive guide to your first multi-agent workflow"`

### author
- **Type**: string
- **Default**: "Eigent"
- **Description**: Author name
- **Example**: `"Eigent Team"`

### authorprofile
- **Type**: string (path)
- **Description**: Path to author profile image
- **Location**: Store in `view/public/blog/author/`
- **Recommended size**: 200x200px (square, displayed as circular)
- **Example**: `"/blog/author/nomad.png"`

### role
- **Type**: string
- **Default**: "Author"
- **Description**: Author's role/title
- **Example**: `"Growth"` or `"Engineering"` or `"Product Manager"`

### description
- **Type**: string
- **Description**: SEO description and preview text for blog cards
- **Recommended length**: 150-160 characters for optimal SEO
- **Example**: `"Learn how to set up your first multi-agent workflow with Eigent in just a few minutes."`

### keywords
- **Type**: array or string
- **Description**: SEO keywords for the post
- **Format options**:
  - Array: `["keyword1", "keyword2", "keyword3"]`
  - String: `"keyword1, keyword2, keyword3"`
- **Example**: `["Eigent", "multi-agent", "tutorial", "getting started"]`

### toc
- **Type**: boolean
- **Default**: `true`
- **Description**: Enable/disable table of contents generation
- **Note**: TOC is automatically generated from headings
- **Example**: `true` or `false`

### cover
- **Type**: string (path)
- **Description**: Path to cover image
- **Location**: Store in `view/public/blog/thumbnail/`
- **Recommended size**: 1200x630px for optimal display
- **Example**: `"/blog/thumbnail/post-thumbnail.png"`

### thumbnail
- **Type**: string (path)
- **Description**: Path to thumbnail image for blog cards
- **Fallback**: Uses `cover` value if not provided
- **Location**: Store in `view/public/blog/thumbnail/`
- **Recommended size**: 1200x630px
- **Example**: `"/blog/thumbnail/your-thumbnail.png"`

### featured
- **Type**: boolean
- **Default**: `false`
- **Description**: Mark post as featured (appears prominently on blog index)
- **Note**: Only feature best/most important posts
- **Example**: `true` or `false`

### category
- **Type**: string
- **Description**: Category name displayed on blog cards
- **Best practice**: Use consistent category names across posts
- **Examples**: `"Tutorial"`, `"Case Study"`, `"News"`, `"Product Update"`

## Complete Example

```yaml
---
title: "Getting Started with Eigent"
subtitle: "A comprehensive guide to your first multi-agent workflow"
date: "2025-01-15"
author: "Eigent Team"
authorprofile: "/blog/author/eigent.png"
role: "Growth"
description: "Learn how to set up your first multi-agent workflow with Eigent in just a few minutes."
keywords: ["Eigent", "multi-agent", "tutorial", "getting started"]
toc: true
thumbnail: "/blog/thumbnail/getting-started.png"
featured: true
category: "Tutorial"
---
```

## Minimal Example

```yaml
---
title: "My Blog Post"
date: "2025-01-15"
---
```