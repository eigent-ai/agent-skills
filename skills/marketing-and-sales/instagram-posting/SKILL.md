---
name: instagram-posting
description: Automates the process of posting to an already logged-in Instagram account using a browser-capable agent. Use this skill when the user requests to post, upload, publish, or share a video or image to Instagram with provided content and tags.
---

# Instagram Posting Workflow

## Overview
This skill guides a browser-capable agent through automating the process of uploading and publishing a post (video or image) to Instagram. It handles media upload, correct aspect ratio cropping, and adding tags/content.

## Workflow Execution Steps

### 1. Identify Media Aspect Ratio
Before opening the browser, calculate the aspect ratio of the media to select the correct crop option on the upload screen.
- Use the bundled script: `python scripts/get_media_aspect_ratio.py <path_to_media_file>`
- The script will output the appropriate crop option: `1:1`, `4:5`, `16:9`, `9:16`, or `Original`.
- Note this exact crop option for use in Step 2.

### 2. Browser Automation: Uploading Media
Using your browser-automation capability (e.g., Playwright or Selenium), navigate to https://www.instagram.com/ and execute the following:
1. **Click 'Add' (Create Post)**: Locate and click the 'New Post' or 'Create' button (often a '+' icon) in the navigation menu.
2. **Upload Provided Video or Image**:
   - To bypass the OS file upload window, locate the hidden `<input type="file">` element on the upload modal and set its value to the absolute path of the media file, or simulate a drag-and-drop of the file into the dropzone.
3. **Select Crop Option**:
   - Once the media is previewed, click the 'Crop' selector button (usually located at the bottom left of the preview).
   - Click the option that corresponds to the ratio identified in Step 1 (e.g., Original, 1:1, 4:5, 16:9, or 9:16).
4. **Click Next**: Proceed past any filter or edit screens by clicking 'Next' until reaching the final share screen.

### 3. Adding Provided Content and Tags
On the final "Create new post" screen:
- Locate the caption/description text area.
- Enter the provided content exactly as requested.
- Append the provided tags (hashtags) to the end of the content.

### 4. Publishing the Post
- Locate and click the 'Share' or 'Publish' button.
- Await confirmation that the post has been shared successfully before concluding the automation task.
