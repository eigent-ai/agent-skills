---
name: eigent-usecase-update
description: Create and manage usecases for the Eigent website. Use when the user wants to add, edit, or work with usecases in the Eigent repository. Triggers include requests to create usecases, add usecase demonstrations, edit existing usecases, generate usecase JSON files, or work with usecase metadata and media assets. Also use when asked about usecase structure, JSON format, or asset organization.
license: Apache-2.0
metadata:
  author: eigent-ai
  version: "1.0"
---

# Eigent Usecase Management

Create and manage usecases for the Eigent website with proper JSON structure, media assets, and SEO optimization.

## Overview

Usecases are stored as JSON files in `public/usecase/posts/`. Each usecase defines a demonstration of Eigent's capabilities with video, description, and metadata. Media assets (images, videos) are stored in `public/gallery/`.

## Quick Start

### Creating a New Usecase

Use the generate_usecase.py script to create a properly formatted JSON file:

```bash
python scripts/generate_usecase.py "Usecase Title" \
  --keywords "keyword1,keyword2,keyword3" \
  --upload-date "2025-08-01" \
  --replay-url "https://www.eigent.ai/download?share_token=YOUR_SHARE_TOKEN" \
  --featured
```

Or create manually with the template:

```json
{
  "id": "usecase_id_in_snake_case",
  "title": "Usecase Title",
  "prompt": "Short description",
  "description": "Full description",
  "image": "/gallery/usecase_id_in_snake_case.png",
  "videoSrc": "/gallery/usecase_id_in_snake_case.mp4",
  "videoPoster": "/gallery/usecase_id_in_snake_case.png",
  "videoTitle": "Usecase Title",
  "replayUrl": "https://www.eigent.ai/download?share_token=YOUR_SHARE_TOKEN",
  "uploadDate": "2025-08-01",
  "featured": false,
  "keywords": ["keyword1", "keyword2"],
  "metaDescription": "SEO description"
}
```

### File Location and URL Mapping

- **Create in**: `public/usecase/posts/your-usecase-id.json`
- **Filename**: Use snake_case matching the `id` field
- **URL**: `/usecases/your-usecase-id` (uses the `id` field)

## JSON Structure

### Required Fields

- `id` (string): Unique identifier in snake_case (used in URL)
- `title` (string): Display title
- `prompt` (string): Short description for card (50-100 chars)
- `description` (string): Full copyable description
- `image` (string): Path to card image (e.g., `/gallery/card.png`)
- `videoSrc` (string): Path to demo video (e.g., `/gallery/demo.mp4`)
- `videoPoster` (string): Path to video poster image
- `videoTitle` (string): Accessibility title for video
- `uploadDate` (string): Upload/publication date in `YYYY-MM-DD` format
- `featured` (boolean): Mark as featured usecase
- `keywords` (array): SEO keywords
- `metaDescription` (string): SEO meta description (150-160 chars)

### Optional Fields

- `replayUrl` (string): URL to replay/demo the usecase

See [json-structure.md](references/json-structure.md) for complete field specifications and examples.

## Directory Structure

```
public/usecase/
├── posts/              # Usecase JSON files
└── _template.json      # Template for new usecases

public/gallery/         # Media assets
├── [card-images]       # 800x600px card images
├── [videos]            # MP4 demo videos
└── [posters]           # Video poster images
```

See [directory-structure.md](references/directory-structure.md) for detailed organization.

## Media Assets

### Card Images
- **Size**: 800x600px or 16:9 aspect ratio
- **Location**: `public/gallery/`
- **Naming**: `{usecase-id}.png`
- **Reference**: `"/gallery/usecase_id_in_snake_case.png"`

### Demo Videos
- **Format**: MP4 (H.264 codec recommended)
- **Location**: `public/gallery/`
- **Naming**: `{usecase-id}.mp4`
- **Reference**: `"/gallery/usecase_id_in_snake_case.mp4"`

### Video Posters
- **Size**: Match video dimensions (can reuse the same image used by `image`)
- **Location**: `public/gallery/`
- **Naming**: `{usecase-id}.png` (or a dedicated poster file if needed)
- **Reference**: `"/gallery/usecase_id_in_snake_case.png"`

## Workflow Steps

When creating a usecase:

1. **Generate JSON** using generate_usecase.py script OR create manually from template
2. **Set required fields**:
   - `id`: Unique snake_case identifier
   - `title`: Display title
   - `prompt`: Short card description (50-100 chars)
   - `description`: Full copyable description
   - `uploadDate`: Date string in `YYYY-MM-DD`
   - `featured`: Boolean for featured status
   - `keywords`: Array of 5-10 SEO keywords
   - `metaDescription`: 150-160 char SEO description

3. **Create media assets**:
   - Card/listing image (800x600px) → `public/gallery/{id}.png`
   - Demo video (MP4) → `public/gallery/{id}.mp4`
   - Video poster → `public/gallery/{id}.png` (or dedicated poster file)

4. **Update JSON paths** to reference media assets

5. **Save to** `public/usecase/posts/{id}.json`

6. **Verify** JSON syntax and asset paths

7. **Optional: Open a PR**:
   - Create a branch (for example: `codex/usecase-{id}`)
   - Commit JSON and media path updates with a clear message
   - Push the branch and open a pull request for review

## Naming Conventions

### Usecase IDs
- **Format**: snake_case (lowercase with underscores)
- **Example**: `generate_financial_report`
- **Used in**: URL and filename

### File Names
- **JSON**: `{id}.json` (e.g., `generate_report.json`)
- **Image**: `{id}.png` (e.g., `generate_report.png`)
- **Video**: `{id}.mp4` (e.g., `generate_report.mp4`)
- **Poster**: `{id}.png` (or a dedicated poster file path if needed)

## Best Practices

1. **Unique IDs**: Ensure each usecase has a unique ID
2. **Descriptive titles**: Use clear, action-oriented titles
3. **Compelling prompts**: Write engaging 50-100 char descriptions
4. **Full descriptions**: Explain value and process clearly
5. **SEO optimization**: Include relevant keywords and meta descriptions
6. **Featured sparingly**: Only feature top usecases
7. **Optimize media**: Compress videos and images
8. **Consistent naming**: Prefer snake_case IDs and matching media filenames

## Template Features

The UsecaseTemplate component provides:
- Large, bold title display
- Copyable description with hover effects
- Centered video player with custom poster
- Replay button functionality
- Responsive design
- SEO optimization with meta tags

## Common Issues

### Usecase Not Appearing
- Check file is in `public/usecase/posts/`
- Verify JSON syntax (use JSON validator)
- Ensure all required fields are present
- Check that filename matches `id` field

### Media Not Loading
- Verify paths start with `/gallery/`
- Check files exist in `public/gallery/`
- Ensure exact filename match (case-sensitive)
- Confirm video is in MP4 format

### URL Issues
- URL uses `id` field from JSON, not filename
- Ensure `id` is in snake_case
- Check for unique IDs across all usecases

## Scripts

- **generate_usecase.py**: Generate usecase JSON files with proper structure
  - Automatically creates valid JSON with all required fields
  - Generates snake_case IDs from titles
  - Supports custom keywords, descriptions, replay URL, upload date, and featured status
  - Provides next steps for asset creation

## Git Handoff (Optional)

Use this when the user asks to ship changes via GitHub:

1. Create a branch with prefix `codex/`.
2. Stage only intended usecase JSON and related media changes.
3. Commit with a clear summary.
4. Open a PR with:
   - Usecase ID/title updated
   - Media assets added or changed
   - Any follow-up items (if applicable)

## Assets

- **_template.json**: Template file for manual usecase creation

## References

- **json-structure.md**: Complete JSON field specifications with validation rules
- **directory-structure.md**: Asset organization and path conventions
