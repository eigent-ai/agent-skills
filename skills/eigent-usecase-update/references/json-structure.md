# Usecase JSON Structure Reference

Complete specification for Eigent usecase JSON files.

## Required Fields

### id
- **Type**: string
- **Description**: Unique identifier used in URLs
- **Format**: Use snake_case (lowercase with underscores)
- **Example**: `"generate_q2_report_from_csv_bank_data"`
- **Note**: Must be unique across all usecases

### title
- **Type**: string
- **Description**: Display title shown on usecase page
- **Example**: `"Generate Q2 Report from CSV Bank Data"`

### prompt
- **Type**: string
- **Description**: Short prompt description for card display
- **Recommended length**: 50-100 characters
- **Example**: `"Analyze financial data and create quarterly reports"`

### description
- **Type**: string
- **Description**: Full detailed description that will be copyable by users
- **Format**: Can be multi-line text
- **Example**: `"Generate a comprehensive Q2 financial report by analyzing CSV bank transaction data, identifying trends, and creating visualized summaries."`

### image
- **Type**: string (path)
- **Description**: Path to the card image displayed in usecase listings
- **Location**: Store in `/gallery/` directory
- **Format**: PNG, JPG, WebP
- **Recommended size**: 800x600px or 16:9 aspect ratio
- **Example**: `"/gallery/generate_q2_report_from_csv_bank_data.png"`

### videoSrc
- **Type**: string (path)
- **Description**: Path to video file demonstrating the usecase
- **Location**: Store in `/gallery/` directory
- **Format**: MP4 (recommended for browser compatibility)
- **Example**: `"/gallery/generate_q2_report_from_csv_bank_data.mp4"`

### videoPoster
- **Type**: string (path)
- **Description**: Path to poster image shown before video plays
- **Location**: Store in `/gallery/` directory
- **Format**: PNG, JPG
- **Recommended size**: Match video dimensions (can reuse `image`)
- **Example**: `"/gallery/generate_q2_report_from_csv_bank_data.png"`

### videoTitle
- **Type**: string
- **Description**: Accessibility title for the video
- **Purpose**: Used for screen readers and video metadata
- **Example**: `"Generate Q2 Report from CSV Bank Data"`

### uploadDate
- **Type**: string
- **Description**: Upload/publication date for the usecase
- **Format**: `YYYY-MM-DD`
- **Example**: `"2025-08-01"`

### featured
- **Type**: boolean
- **Description**: Mark usecase as featured (appears prominently)
- **Values**: `true` or `false`
- **Default**: `false`
- **Note**: Only feature your best/most impactful usecases

### keywords
- **Type**: array of strings
- **Description**: SEO keywords for the usecase page
- **Recommended count**: 5-10 keywords
- **Format**: `["keyword1", "keyword2", "keyword3"]`
- **Example**: `["financial", "reporting", "CSV", "analysis", "automation"]`

### metaDescription
- **Type**: string
- **Description**: SEO meta description for the page
- **Recommended length**: 150-160 characters
- **Example**: `"Automate Q2 financial reporting by analyzing CSV bank data with Eigent's multi-agent workflow system."`

## Optional Fields

### replayUrl
- **Type**: string (URL)
- **Description**: Optional URL to replay/demo the usecase
- **Example**: `"https://app.eigent.com/replay/q2-report-demo"`
- **Note**: Can be omitted if not applicable

## Complete Example

```json
{
  "id": "generate_q2_report_from_csv_bank_data",
  "title": "Generate Q2 Report from CSV Bank Data",
  "prompt": "Analyze financial data and create quarterly reports",
  "description": "Generate a comprehensive Q2 financial report by analyzing CSV bank transaction data, identifying trends, and creating visualized summaries with charts and insights.",
  "image": "/gallery/generate_q2_report_from_csv_bank_data.png",
  "videoSrc": "/gallery/generate_q2_report_from_csv_bank_data.mp4",
  "videoPoster": "/gallery/generate_q2_report_from_csv_bank_data.png",
  "videoTitle": "Generate Q2 Report from CSV Bank Data",
  "replayUrl": "https://app.eigent.com/replay/q2-report-demo",
  "uploadDate": "2025-08-01",
  "featured": true,
  "keywords": [
    "financial reporting",
    "CSV analysis",
    "bank data",
    "quarterly report",
    "automation",
    "data visualization"
  ],
  "metaDescription": "Automate Q2 financial reporting by analyzing CSV bank data with Eigent's multi-agent workflow system. Generate insights and visualizations instantly."
}
```

## Minimal Example

```json
{
  "id": "simple_usecase",
  "title": "Simple Usecase",
  "prompt": "Brief description",
  "description": "Full description of what this usecase does.",
  "image": "/gallery/simple_usecase.png",
  "videoSrc": "/gallery/simple_usecase.mp4",
  "videoPoster": "/gallery/simple_usecase.png",
  "videoTitle": "Simple Usecase Demo",
  "uploadDate": "2025-08-01",
  "featured": false,
  "keywords": ["keyword1", "keyword2"],
  "metaDescription": "Simple usecase demonstration with Eigent."
}
```

## Field Validation Rules

- **id**: Must be unique, snake_case, no spaces or special characters
- **title**: Required, non-empty string
- **prompt**: Required, recommended 50-100 chars
- **description**: Required, can be multi-line
- **image**: Must be valid path starting with `/`
- **videoSrc**: Must be valid path starting with `/`
- **videoPoster**: Must be valid path starting with `/`
- **videoTitle**: Required for accessibility
- **uploadDate**: Required, must be `YYYY-MM-DD`
- **featured**: Must be boolean (true/false)
- **keywords**: Must be array, recommended 5-10 items
- **metaDescription**: Required, recommended 150-160 chars
- **replayUrl**: Optional, must be valid URL if provided
