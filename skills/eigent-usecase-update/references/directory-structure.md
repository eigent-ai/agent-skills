# Eigent Usecase Directory Structure

Complete directory structure and asset organization for the Eigent usecase system.

## Main Directories

```
public/usecase/
├── posts/              # Usecase JSON files
└── _template.json      # Template file for new usecases

public/gallery/         # Media assets for usecases
├── [card-images]/      # Card images for usecase listings
├── [videos]/           # Demo videos
└── [posters]/          # Video poster images
```

## Directory Details

### public/usecase/posts/
- **Purpose**: Store all usecase JSON configuration files
- **File naming**: Use snake_case matching the `id` field
- **Extension**: `.json`
- **Example**: `generate_q2_report.json`

### public/gallery/
- **Purpose**: Store all media assets for usecases
- **Subdirectories**: Optional - can organize by usecase or type
- **Asset types**:
  - Card images (displayed in usecase listings)
  - Demo videos (MP4 format recommended)
  - Video posters (shown before video plays)

## File Naming Conventions

### Usecase JSON Files
- **Format**: `{usecase-id}.json`
- **Case**: snake_case (lowercase with underscores)
- **Examples**:
  - `generate_q2_report.json`
  - `analyze_customer_data.json`
  - `automate_email_responses.json`

### Media Assets
- **Card images**: `{usecase-id}-card.png`
- **Videos**: `{usecase-id}-demo.mp4`
- **Posters**: `{usecase-id}-poster.png`

**Examples**:
- `/gallery/q2-report-card.png`
- `/gallery/q2-report-demo.mp4`
- `/gallery/q2-report-poster.png`

## URL Structure

### Usecase Pages
- **Pattern**: `/usecases/[id]`
- **Example**: `/usecases/generate_q2_report_from_csv_bank_data`
- **Note**: URL uses the `id` field from JSON file

### Asset URLs
All assets referenced in JSON files use absolute paths:
- Card image: `/gallery/usecase-card.png`
- Video: `/gallery/usecase-demo.mp4`
- Poster: `/gallery/usecase-poster.png`

## Path Examples

### Usecase Files
- `public/usecase/posts/generate_q2_report.json`
- `public/usecase/posts/analyze_customer_data.json`
- `public/usecase/posts/automate_workflows.json`

### Media Assets
- `public/gallery/q2-report-card.png`
- `public/gallery/q2-report-demo.mp4`
- `public/gallery/q2-report-poster.png`
- `public/gallery/customer-data-card.png`
- `public/gallery/customer-data-demo.mp4`

## Template File

Located at `public/usecase/_template.json`, this file serves as:
- Starting point for new usecases
- Reference for required fields
- Example structure

**Note**: Files starting with `_` are not processed as usecases.

## Media Specifications

### Card Images
- **Recommended size**: 800x600px or 16:9 aspect ratio
- **Format**: PNG, JPG, WebP
- **Purpose**: Displayed in usecase listing cards
- **Location**: `/gallery/`

### Videos
- **Format**: MP4 (best browser compatibility)
- **Codec**: H.264
- **Purpose**: Demo video on usecase page
- **Location**: `/gallery/`

### Video Posters
- **Size**: Match video dimensions
- **Format**: PNG, JPG
- **Purpose**: Shown before video plays
- **Location**: `/gallery/`

## Workflow Example

When adding a new usecase "analyze_sales_data":

1. **Create JSON**: `public/usecase/posts/analyze_sales_data.json`
2. **Add card image**: `public/gallery/analyze-sales-card.png`
3. **Add video**: `public/gallery/analyze-sales-demo.mp4`
4. **Add poster**: `public/gallery/analyze-sales-poster.png`
5. **Set paths in JSON**:
   ```json
   {
     "id": "analyze_sales_data",
     "image": "/gallery/analyze-sales-card.png",
     "videoSrc": "/gallery/analyze-sales-demo.mp4",
     "videoPoster": "/gallery/analyze-sales-poster.png"
   }
   ```
6. **Access at**: `/usecases/analyze_sales_data`

## Best Practices

1. **Consistent naming**: Use snake_case for IDs, kebab-case for files
2. **Logical organization**: Group related assets together
3. **Descriptive names**: Make file purposes clear
4. **Asset optimization**: Compress images and videos
5. **Path accuracy**: Always use absolute paths starting with `/`
6. **Case sensitivity**: Remember URLs and paths are case-sensitive